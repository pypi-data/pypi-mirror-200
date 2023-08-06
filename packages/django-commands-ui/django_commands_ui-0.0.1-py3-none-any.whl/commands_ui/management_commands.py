import argparse
import contextlib
import functools
import io
import tempfile
import traceback
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from django.core import management
from django.core.management import base

from commands_ui import app_settings, domain, models, patch

if TYPE_CHECKING:

    class User:
        pass

else:
    User = models.get_user_model()


class EmptyStringIO(io.StringIO):
    """This StringIO will always be empty."""

    _VALUE = ""

    def getvalue(self) -> str:
        return self._VALUE

    def seek(self, *args, **kwargs) -> int:
        return 0

    def read(self, *args, **kwargs) -> str:
        return self.getvalue()

    def readline(self, *args, **kwargs) -> str:  # type: ignore[override]
        return self.getvalue()

    def readlines(self, *args, **kwargs) -> list[str]:  # type: ignore[override]
        return [self.getvalue()]

    def write(self, *args, **kwargs) -> int:
        return 0

    def writelines(self, *args, **kwargs) -> None:
        pass

    def truncate(self, *args, **kwargs) -> int:
        return 0


class BaseManagementCommand(base.BaseCommand):
    """Base ManagementCommand class here we can add methods and attribute that we want to share on
    all management classes

    Lets an optional arguments property to be specified: allow modification of the parser and preprocessing of
    handler arguments. This enables commands to compose common parser setups
    """

    def create_parser(
        self, prog_name: str, subcommand: str, **kwargs
    ) -> base.CommandParser:
        parser = super().create_parser(prog_name, subcommand)
        for custom_argument in getattr(self, "arguments", []):
            custom_argument.modify_parser(parser)

        return parser

    def execute(self, *args, **options) -> str | None:
        for custom_argument in getattr(self, "arguments", []):
            args, options = custom_argument.pre_execute(*args, **options)

        return super().execute(*args, **options)

    def warning(self, s: str) -> None:
        self.stdout.write(self.style.WARNING(s))

    def error(self, s: str) -> None:
        self.stderr.write(self.style.ERROR(s))

    def notice(self, s: str) -> None:
        self.stdout.write(self.style.NOTICE(s))

    def success(self, s: str) -> None:
        self.stdout.write(self.style.SUCCESS(s))


class JobBasedCommand(BaseManagementCommand):
    """
    This class gives the possibility of updating a Job instance status output while it's being run,
    with the following features:

    - adds an optional job_id argument, that will be passed to the management command when being
      run from Jobs UI.
    - when the job_id is given, the job instance will be fetched and set on the management command
      instance.
    - adds a print function that can be used by management commands that will print the given
      message to the standard output and update the job instance output. This is used for updating
      the status of a job being run.
    """

    job: models.Job | None = None
    output: io.StringIO = EmptyStringIO()
    redirected_print: patch.PatchedPrint = patch.LoggedPrint()
    exit_stack: contextlib.ExitStack | None = None

    def create_parser(
        self, prog_name: str, subcommand: str, **kwargs
    ) -> base.CommandParser:
        """
        Add an optional job-id argument to the command.
        """
        parser = super().create_parser(prog_name, subcommand)
        parser.add_argument("--job-id", type=int)
        self.exit_stack = contextlib.ExitStack()

        # mypy doesn't understand callables well enough
        parser.parse_args = functools.partial(  # type:ignore
            self._parse_preprocessed_args_with, parser.parse_args
        )

        return parser

    def _parse_preprocessed_args_with(
        self,
        base_parse_args: Callable[..., argparse.Namespace],
        args=None,
        namespace=None,
    ) -> argparse.Namespace:
        if args is not None:
            assert self.exit_stack is not None, "should be set in create_parser"
            temp_directory_name = self.exit_stack.enter_context(
                tempfile.TemporaryDirectory()
            )
            processed_args = domain.get_preprocessed_command_arguments(
                None, args, temp_directory_name
            )
            if processed_args is not None:
                return base_parse_args(args=processed_args, namespace=namespace)
        return base_parse_args(args=args, namespace=namespace)

    def execute(self, *args, **options) -> str | None:
        """
        If there's a job_id in the command arguments, fetch it and set it in the command instance.
        """
        job_id = options.get("job_id")

        if job_id:
            try:
                # Read from the primary DB, not a replica, because the Job was likely just created.
                self.job = models.Job.objects.using(app_settings.DATABASE_PRIMARY).get(
                    id=job_id
                )
            except models.Job.DoesNotExist:
                pass
            else:
                assert self.job is not None, "job_id should be an exiting ID"
                if not domain.should_run(self.job):
                    return None
                self.job.mark_as_started()

                self.output = io.StringIO()
                self.redirected_print = patch.RedirectedPrint(destination=self.output)

        assert self.exit_stack is not None, "should be set in create_parser"

        ending_reason = ""
        try:
            return super().execute(*args, **options)
        except management.CommandError as e:
            # CommandError indicates an anticipated failure; just print the error message
            # without the stacktrace.
            ending_reason = str(e)
            raise
        except Exception:
            ending_reason = traceback.format_exc(chain=True)
            raise
        finally:
            if ending_reason:
                self.print(ending_reason)
            if self.job:
                self.job.mark_as_finished(self.output.getvalue())

    def print(self, message: Any) -> None:
        """
        Print the given message.

        This will also end up in the job's output, if there is one.
        """
        # Only print to stdout if CRON env-var isn't set, or is false
        if not app_settings.CRON_ENVIRONMENT:
            self.redirected_print.redirected_print(message)

    def warning(self, s: str) -> None:
        self.print(self.style.WARNING(s))

    def error(self, s: str) -> None:
        self.print(self.style.ERROR(s))

    def notice(self, s: str) -> None:
        self.print(self.style.NOTICE(s))

    def success(self, s: str) -> None:
        self.print(self.style.SUCCESS(s))

    @property
    def user(self) -> User | None:
        """
        Get the user who is running this job, or politely warn if we are not running inside
        a job.
        """
        if self.job:
            return self.job.created_by

        self.print(
            "This command is not being run as a job but we are trying to get a user for it"
        )
        return None
