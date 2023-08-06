from django.conf import settings
from django.utils.module_loading import import_string

USER_MODEL = getattr(settings, "COMMANDS_UI_USER_MODEL", settings.AUTH_USER_MODEL)

CELERY_APP = getattr(settings, "COMMANDS_UI_CELERY_APP")

# Database identifiers
DATABASE_PRIMARY = getattr(settings, "DATABASE_PRIMARY", "default")

# Define if this is a cron environment
CRON_ENVIRONMENT = getattr(settings, "CRON_ENVIRONMENT", False)

# List of apps from we want to extract the runnable commands
COMMANDS_UI_JOB_APPS = getattr(settings, "COMMANDS_UI_JOB_APPS", "")

# Working celery queue name for standard jobs
COMMANDS_UI_JOBS_QUEUE = getattr(settings, "COMMANDS_UI_JOBS_QUEUE", "")

# Media path
MEDIA_URL = getattr(settings, "MEDIA_URL", "")
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", "")

# Storage
DOCUMENT_STORAGE_BACKEND = getattr(settings, "DOCUMENT_STORAGE_BACKEND", "")
AWS_S3_ENDPOINT_URL = getattr(settings, "AWS_S3_ENDPOINT_URL", "")
S3_MANAGEMENT_COMMAND_UPLOADS_BUCKET = getattr(
    settings, "S3_MANAGEMENT_COMMAND_UPLOADS_BUCKET", ""
)

app = import_string(CELERY_APP)
