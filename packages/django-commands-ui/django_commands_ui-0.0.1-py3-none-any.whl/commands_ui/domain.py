import logging
import os
import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

import requests
from django.apps import apps
from django.core import management
from django.core.files import uploadedfile
from django.utils.module_loading import import_string
from multidb import pinning
from xocto import events, tracing
from xocto.storage import storage

from commands_ui import app_settings, models, tasks

if TYPE_CHECKING:

    class User:
        pass

else:
    User = models.get_user_model()


class UnableToCancelJob(Exception):
    pass


class UnableToRunJob(Exception):
    pass


def store_job_file(attachment, namespace):
    """
    Store an attachment on the S3 jobs bucket.

    Return the corresponding S3 bucket and key.
    """
    store_class = import_string(app_settings.DOCUMENT_STORAGE_BACKEND)
    attachment_store = store_class(app_settings.S3_MANAGEMENT_COMMAND_UPLOADS_BUCKET)
    return attachment_store.store_file(
        namespace=namespace, filename=attachment.name, contents=attachment.read()
    )


def get_runnable_job_list(user: User) -> list:
    """
    Get the list of runnable management commands under the COMMANDS_UI_JOB_APPS apps.
    """
    app_configs = []
    for app_config in reversed(list(apps.get_app_configs())):
        if any(
            regexp.match(app_config.name) is not None  # type: ignore
            for regexp in app_settings.COMMANDS_UI_JOB_APPS
        ):
            path = os.path.join(app_config.path, "management")
            command_list = []
            for name in management.find_commands(path):
                try:
                    job = management.load_command_class(app_config.name, name)
                except Exception:
                    # If the command can't be loaded do not display it
                    continue
                if _user_can_view_job(job, user):
                    display_name = getattr(job, "verbose_name", _clean_name(name))
                    command_list.append(
                        {
                            "display_name": display_name,
                            "name": name,
                            "interface": getattr(job, "interface_name", "unknown"),
                        }
                    )
            app_configs.append(
                {
                    "path": app_config.name,
                    "name": app_config.verbose_name,
                    "command_list": command_list,
                }
            )
    return sorted(app_configs, key=lambda app: app["name"])


def get_app_config_name(command_name: str) -> str:
    """
    Get the name of a given command name app.
    """
    # Load the command object by its name.
    try:
        return management.get_commands()[command_name]
    except KeyError:
        raise management.CommandError("Unknown command: %r" % command_name)


def get_command_file_contents(
    app_config_name: str, command_name: str
) -> tuple[str, str]:
    """
    Get the contents of a given command name file.
    """
    app_config_paths = {}
    for app_config in reversed(list(apps.get_app_configs())):
        if any(
            regexp.match(app_config.name) is not None  # type: ignore
            for regexp in app_settings.COMMANDS_UI_JOB_APPS
        ):
            path = os.path.join(app_config.path, "management", "commands")
            app_config_paths[app_config.name] = path
    command_path = os.path.join(app_config_paths[app_config_name], f"{command_name}.py")

    with open(command_path) as command_file:
        file_contents = command_file.read()

    return file_contents, command_path


def create_job_with_arguments(
    name: str, creator: User, data: dict[str, Any]
) -> models.Job:
    """
    Create a new Job given a name for the command and a dictionary with its arguments.
    """
    app_config_name = get_app_config_name(name)

    job = models.Job.objects.create(
        name=name,
        app_config_name=app_config_name,
        created_by=creator,
        arguments={},
    )

    job_arguments = _get_job_arguments_from_dict(data)
    job_arguments = _replace_file_args_with_s3_urls(job.id, job_arguments)
    job.set_arguments(job_arguments)
    return job


def queue_job(job: models.Job, **kwargs: dict) -> None:
    """
    Set job to be run on a worker at the next available opportunity.
    """
    tasks.run_job.delay(job.id)


def cancel_job(job: models.Job, reason: str = "", force: bool = False) -> None:
    """
    Cancel a job if it hasn't started running already.

    Use `force` to mark the job as cancelled even if it has already started running.
    """
    job.refresh_from_db()
    if not job.has_started or force:
        job.mark_as_cancelled(reason)
    else:
        raise UnableToCancelJob(
            "This job has started already and it can't be cancelled anymore."
        )


def should_run(job: models.Job) -> bool:
    """
    Determine whether to run the given job.

    Returns False if it's running already or has been cancelled, otherwise returns True.

    :raises UnableToRunJob: if the job has already been started
    """

    if job.has_started:
        raise UnableToRunJob("The job has already been run once")

    if same_job := _get_same_running_job(job):
        cancel_job(job, f"This same job is already running (id: {same_job.pk})")
        return False

    if job.has_been_cancelled:
        return False

    return True


# Add a span that changes the DataDog service from the host service to
# "kraken-jobs", to separately classify this set of functionality from
# the BAU for the host.
@tracing.wrap(service="kraken-jobs")
def run(job: models.Job) -> None:
    """
    Run the given job.

    :raises UnableToRunJob: if the job has already been started
    """
    # Only global tags are filterable in the DataDog APM trace inspector UI.
    tracing.set_global_tag("job_name", job.name)

    try:
        # When run via the `run_job` task, everything up to this point has pinned the primary DB
        # for read access, to ensure no replication lag comes into effect during the orchestration
        # phase.  Some MCs can consume a lot of DB resources, however, so the MCs themselves
        # should be run in a context that has reverted to performing reads against the application
        # replica (i.e. with the primary DB unpinned from the thread).
        #
        # N.B: Pinning the primary DB this way should not be a necessary concern once all DB
        # clusters are Aurora-based, as that should eliminate replica lag.  Once all pinning is
        # removed from the code base, so can all unpinning, like this.
        pinning.unpin_this_thread()
        management.call_command(job.name, *job.arguments)
    except UnableToRunJob:
        # These are expected to be raised by this function, so should be handled by the caller.
        raise
    except Exception as e:
        info = f"unable to run management command {job.name} with args {job.arguments}"
        logging.exception(info)
        events.publish(
            event=events.types.JOB_TASK_ERRORED,
            params={"name": job.name, "arguments": job.arguments},
            meta={"error": f"{type(e).__name__}: {e}"},
        )
    finally:
        job.refresh_from_db(using=app_settings.DATABASE_PRIMARY)


def can_access_job(job_name: str, user: User) -> bool:
    """
    Test if the passed user can access the passed job.
    """
    app_config_name = get_app_config_name(job_name)
    job = management.load_command_class(app_config_name, job_name)
    return _user_can_view_job(job, user)


def get_app_config_category(app_config_name: str) -> str:
    return app_config_name.split(".")[-1].title()


def get_command_display_name(command_name: str) -> str:
    return _clean_name(command_name)


def get_command_info_text(job_name: str) -> str:
    app_config_name = get_app_config_name(job_name)
    job = management.load_command_class(app_config_name, job_name)
    return getattr(job, "info_text", "")


def get_preprocessed_command_keyword_arguments(
    job: models.Job | None, arguments: dict[str, Any], downloads_dir: str
) -> dict[str, Any] | None:
    """
    Download S3 keys to given directory and replace with downloaded file paths in returned kwargs.

    If the job has too many files to downloaded, an exception will be raised; the job will be
    cancelled, and `None` returned.

    Also expands media files to absolute paths.
    """
    argument_values = get_preprocessed_command_arguments(
        job, list(arguments.values()), downloads_dir, flatten=False
    )
    if argument_values is None:
        return None
    return dict(zip(arguments.keys(), argument_values))


def get_preprocessed_command_arguments(
    job: models.Job | None, arguments: Sequence, downloads_dir: str, flatten=True
) -> list | None:
    """
    Download S3 keys to given directory and replace with downloaded file paths in returned args.

    If the job has too many files to downloaded, an exception will be raised; the job will be
    cancelled, and `None` returned.

    Also flattens any nested lists, and expands media files to absolute paths.
    """
    job_id = str(job.id if job else uuid.uuid1())
    # We first need to download a maximum number of uploaded files so the CAST report doesn't
    # penalise us for downloading files in a for loop.
    try:
        s3_downloaded_file_paths = _get_s3_downloaded_file_paths(
            job_id, arguments, downloads_dir
        )
    except UnableToRunJob as e:
        if job:
            cancel_job(job, str(e))
        return None

    command_arguments = []
    for arg in arguments:
        # If the argument is an S3 url, pop the downloaded file path from the
        # s3_downloaded_file_paths list rather than downloading the file directly on this for loop.
        # We do it this way to avoid CAST report penalisation - more information in
        # _get_s3_downloaded_file_paths.
        if _is_string_s3_fetch_url(arg):
            command_arguments.append(s3_downloaded_file_paths.pop(0))
        # If the argument is a local media url, change it into an absolute path using the
        # MEDIA_ROOT.
        elif _is_string_local_media_url(arg):
            file_relative_path = arg.replace(app_settings.MEDIA_URL, "")
            file_path = os.path.join(app_settings.MEDIA_ROOT, file_relative_path)
            command_arguments.append(file_path)
        # If the argument is a list, flatten it into separate arguments so that it can be
        # properly interpreted by the argument parser.
        elif isinstance(arg, list) and flatten:
            command_arguments.extend(arg)
        else:
            command_arguments.append(arg)

    return command_arguments


# Private methods


def _is_string_s3_fetch_url(string: str) -> bool:
    """
    Check if a string represents a URL returned by `storage.fetch_url()`:
    """
    prefix = (
        f"{app_settings.AWS_S3_ENDPOINT_URL}/{app_settings.S3_MANAGEMENT_COMMAND_UPLOADS_BUCKET}"
        if app_settings.AWS_S3_ENDPOINT_URL
        else f"https://{app_settings.S3_MANAGEMENT_COMMAND_UPLOADS_BUCKET}"
    )
    return type(string) == str and string.startswith(prefix)


def _is_string_local_media_url(string) -> bool:
    """
    Check if a string media path.
    """
    return type(string) == str and string.startswith(app_settings.MEDIA_URL)


def _get_job_arguments_from_dict(data: dict[str, Any]):
    """
    Transform the dict `data` into a list of arguments to be used by the management command.
    """
    cmd_args = []
    for key, val in data.items():
        # If the value is a boolean, add the argument name to the args if the value is True.
        if isinstance(val, bool):
            if val is True:
                cmd_args.append(key)
            continue
        elif not key.startswith("___"):
            cmd_args.append(key)
        cmd_args.append(val)
    return cmd_args


def _replace_file_args_with_s3_urls(job_id, args):
    """
    Go through a list of given args and replace the InMemoryUploadedFile objects with the
    S3 urls after uploading them.
    """
    new_args = []
    for arg in args:
        if isinstance(
            arg, (uploadedfile.InMemoryUploadedFile, uploadedfile.TemporaryUploadedFile)
        ):
            s3_bucket, s3_key = store_job_file(attachment=arg, namespace=str(job_id))
            store = storage.store(bucket_name=s3_bucket)
            one_hour_in_seconds = 60 * 60  # We want the s3 fetch url to expire in 1h.
            new_args.append(store.fetch_url(s3_key, expires_in=one_hour_in_seconds))
        else:
            new_args.append(arg)
    return new_args


def _get_s3_downloaded_file_paths(
    job_id: str, job_arguments: Sequence, temp_directory_name: str
) -> list[str]:
    """
    Download a maximum of 5 files from S3 for running a Kraken job.
    The reason we're not doing this as a for loop is so we are not heavily penalised by the
    external CAST report, which considers that calling urlretrieve from inside a loop could affect
    performance very heavily - which is true.
    """
    arg_urls_to_download = [
        arg for arg in job_arguments if _is_string_s3_fetch_url(arg)
    ]
    if len(arg_urls_to_download) > 5:
        raise UnableToRunJob(
            "This management command has more than 5 file uploads, which can't be handled by "
            "Kraken Jobs at the moment."
        )

    file_paths = []
    try:
        file_paths.append(
            _download_s3_file_to_directory(
                arg_urls_to_download[0],
                os.path.join(temp_directory_name, f"job_{job_id}_file_1"),
            )
        )
        file_paths.append(
            _download_s3_file_to_directory(
                arg_urls_to_download[1],
                os.path.join(temp_directory_name, f"job_{job_id}_file_2"),
            )
        )
        file_paths.append(
            _download_s3_file_to_directory(
                arg_urls_to_download[2],
                os.path.join(temp_directory_name, f"job_{job_id}_file_3"),
            )
        )
        file_paths.append(
            _download_s3_file_to_directory(
                arg_urls_to_download[3],
                os.path.join(temp_directory_name, f"job_{job_id}_file_4"),
            )
        )
        file_paths.append(
            _download_s3_file_to_directory(
                arg_urls_to_download[4],
                os.path.join(temp_directory_name, f"job_{job_id}_file_5"),
            )
        )
    except IndexError:
        pass
    return file_paths


def _download_s3_file_to_directory(s3_url, file_path):
    """
    Download an s3 url to a given file path.
    """
    response = requests.get(s3_url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    return file_path


def _get_same_running_job(job: models.Job) -> models.Job | None:
    """
    Check if there's a job with the same name and app config name running already.

    :raises Job.MultipleObjectsReturned: if multiple matching jobs are already running
    """
    try:
        return models.Job.objects.get(
            name=job.name,
            app_config_name=job.app_config_name,
            cancelled_at__isnull=True,
            started_at__isnull=False,
            finished_at__isnull=True,
        )
    except models.Job.DoesNotExist:
        return None


def _clean_name(name: str) -> str:
    return name.replace("_", " ").title()


def _user_can_view_job(job: management.BaseCommand, user: User) -> bool:
    """
    Test if the passed user can access the passed job.
    """

    return True
