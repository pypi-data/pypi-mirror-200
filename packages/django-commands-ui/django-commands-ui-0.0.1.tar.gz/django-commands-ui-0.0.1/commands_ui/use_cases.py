from typing import TYPE_CHECKING, Any

from commands_ui import app_settings

from . import domain
from . import models as job_models

if TYPE_CHECKING:
    User = domain.User
else:
    User = app_settings.USER_MODEL


def launch_job_with_arguments(
    command_name: str, creator: User, data: dict[str, Any], **options
) -> job_models.Job:
    """
    Create a new Job to run the MC with the given name, then set it to run.

    Also establishes who was the creator of the Job, and the data context in which it should run.
    """
    new_job = domain.create_job_with_arguments(
        name=command_name, creator=creator, data=data
    )

    domain.queue_job(new_job, **options)
    return new_job
