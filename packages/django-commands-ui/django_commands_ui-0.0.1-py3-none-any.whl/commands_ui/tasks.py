import types

from celery.worker import request
from multidb import pinning

from commands_ui import app_settings
from commands_ui import domain as jobs
from commands_ui import models as data_models


@app_settings.app.task(queue=app_settings.COMMANDS_UI_JOBS_QUEUE, soft_time_limit=3600)
# Read from the primary DB, not a replica, because the Job was likely just created.
@pinning.use_primary_db
def run_job(job_id: int) -> None:
    """
    Run a given Job.
    """
    job = data_models.Job.objects.get(id=job_id)

    if job.has_started:
        # Task has been restarted, likely because it was unexpected terminated.
        # Jobs are not guaranteed to be idempotent so cancel the job and abort the task.
        jobs.cancel_job(job, reason="Task was terminated", force=True)
        return

    jobs.run(job)


@app_settings.app.task(queue=app_settings.COMMANDS_UI_JOBS_QUEUE, soft_time_limit=3600)
# Read from the primary DB, not a replica, because the Job was likely just created.
@pinning.use_primary_db
def mark_job_task_as_failed(
    request: request.Request,
    exc: Exception,
    traceback: types.TracebackType,
    *,
    job_id: int,
    error_message: str,
    **kwargs,
) -> None:
    """
    handle an error for a task and mark a job with the error and error_message
    """
    job = data_models.Job.objects.get(id=job_id)
    job.mark_with_error(error_message.format(job=job_id))


@app_settings.app.task(queue=app_settings.COMMANDS_UI_JOBS_QUEUE, soft_time_limit=3600)
# Read from the primary DB, not a replica, because the Job was likely just created.
@pinning.use_primary_db
def mark_job_task_as_succeeded(job_id: int, success_message: str, **kwargs) -> None:
    """
    handle a success for a task and mark a job with the sucess message
    """
    job = data_models.Job.objects.get(id=job_id)
    job.mark_with_success(success_message)
