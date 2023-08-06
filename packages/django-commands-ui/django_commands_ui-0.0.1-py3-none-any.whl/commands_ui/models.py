from django.apps import apps as django_apps
from django.core import exceptions
from django.db import models
from django.db.models import functions
from xocto import localtime

from commands_ui import app_settings


class Job(models.Model):
    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    name = models.CharField(max_length=256)
    app_config_name = models.CharField(max_length=256)
    output = models.TextField(blank=True)
    arguments = models.JSONField(blank=True, null=True)

    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        app_settings.USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="jobs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields used to track job progress
    task_count = models.PositiveIntegerField(blank=True, null=True)
    task_error_count = models.PositiveIntegerField(blank=True, null=True)
    task_success_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.id}: {self.name} - {self.app_config_name}"

    @property
    def has_finished(self) -> bool:
        """
        Check if the job has been marked as finished and all tasks have been run.
        """
        return bool(self.finished_at) and self.has_finished_tasks

    @property
    def has_finished_tasks(self) -> bool:
        return (self.task_count or 0) == (self.task_error_count or 0) + (
            self.task_success_count or 0
        )

    @property
    def has_started(self):
        return bool(self.started_at)

    @property
    def has_been_cancelled(self):
        return bool(self.cancelled_at)

    @property
    def is_in_progress(self):
        return (
            self.has_started and not self.has_finished and not self.has_been_cancelled
        )

    # Mutators

    def set_arguments(self, arguments) -> None:
        arguments += ["--job-id", self.pk]
        self.arguments = arguments
        self.save()

    def mark_as_started(self) -> None:
        self.started_at = localtime.now()
        self.output = ""
        self.save(update_fields=("started_at", "output"))

    def mark_as_cancelled(self, cancellation_reason: str) -> None:
        self.cancelled_at = localtime.now()
        self.output = models.functions.Concat(
            models.F("output"), models.Value(cancellation_reason)
        )
        self.save(update_fields=("output", "cancelled_at"))

    def mark_as_finished(self, output: str) -> None:
        self.finished_at = localtime.now()
        self.output = _append_output(output)
        self.save(update_fields=("output", "finished_at"))

    def increment_task_count(self, output: str) -> None:
        self.task_count = functions.Coalesce(models.F("task_count"), 0) + 1
        self.output = _append_output(output)
        self.save(update_fields=["output", "task_count"])

    def mark_with_success(self, message: str) -> None:
        self.task_success_count = (
            functions.Coalesce(models.F("task_success_count"), 0) + 1
        )
        self.output = _append_output(message)
        self.save(update_fields=("output", "task_success_count"))

    def mark_with_error(self, message: str) -> None:
        self.task_error_count = functions.Coalesce(models.F("task_error_count"), 0) + 1
        self.output = _append_output(message)
        self.save(update_fields=("output", "task_error_count"))


def _append_output(new_output: str) -> models.Func:
    return models.functions.Concat(models.F("output"), models.Value(f"{new_output}"))


def get_user_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(app_settings.USER_MODEL, require_ready=False)
    except ValueError:
        raise exceptions.ImproperlyConfigured(
            "USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise exceptions.ImproperlyConfigured(
            "USER_MODEL refers to model '%s' that has not been installed"
            % app_settings.USER_MODEL
        )
