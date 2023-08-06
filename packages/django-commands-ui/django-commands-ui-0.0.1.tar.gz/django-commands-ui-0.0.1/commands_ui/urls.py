from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    # Balance URLs
    path("", views.JobList.as_view(), name="jobs"),
    path("history/", views.JobHistory.as_view(), name="job-history"),
    path("detail/<str:command_name>/", views.Job.as_view(), name="job"),
    path("status/<int:pk>/", views.JobStatus.as_view(), name="job-status"),
    path("output/<int:pk>/", views.JobOutput.as_view(), name="job-output"),
]
