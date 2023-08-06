from django import http, shortcuts, urls
from django.contrib import messages
from django.core import exceptions, management
from django.http import response
from django.views import generic
from rest_framework import serializers
from xocto import types

from commands_ui import domain, forms, models
from commands_ui import use_cases as job_usecases

User = models.get_user_model()


class HasJobsAccess:
    """Allow access to a view if user has access to at least one job."""

    def dispatch(self, request, *args, **kwargs):
        self.runnable_jobs = domain.get_runnable_job_list(self.request.user)
        self.runnable_jobs_names = []
        for app_jobs in self.runnable_jobs:
            self.runnable_jobs_names.extend(
                _x.get("name") for _x in app_jobs.get("command_list", [])
            )
        if not self.runnable_jobs_names:
            raise exceptions.PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class JobList(HasJobsAccess, generic.TemplateView):
    template_name = "jobs/job-list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["runnable_job_list"] = self.runnable_jobs
        return ctx


class JobHistory(HasJobsAccess, generic.ListView):
    model = models.Job
    context_object_name = "job_list"
    template_name = "jobs/job-history.html"
    paginate_by = 50

    class JobHistoryTemplateSerializer(serializers.Serializer):
        pk = serializers.IntegerField()
        name = serializers.SerializerMethodField()
        created_at = serializers.CharField()
        created_by = serializers.CharField()
        started_at = serializers.CharField()
        finished_at = serializers.CharField()
        cancelled_at = serializers.CharField()

        def get_name(self, obj):
            return str(obj)

    serializer_class = JobHistoryTemplateSerializer

    def dispatch(self, request, *args, **kwargs):
        # Initialise the filters form.
        self.filters_form = forms.JobFilterForm(request.GET)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_filtered_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters_form"] = self.filters_form
        return context

    def get_filtered_queryset(self):
        """
        Return a queryset after filtering the base queryset results.
        """
        queryset = self.model.objects.filter(name__in=self.runnable_jobs_names)
        filtered_queryset = self._filter_by_filters_form(queryset)
        return filtered_queryset

    def _filter_by_filters_form(self, qs):
        """
        Filter jobs by the user who created it.
        """
        if not self.filters_form.is_valid():
            return qs

        form_data = self.filters_form.cleaned_data

        if form_data["created_by"]:
            qs = qs.filter(created_by__id=form_data["created_by"])

        if form_data["job_name_search"]:
            qs = qs.filter(name__contains=form_data["job_name_search"])

        return qs


class Job(generic.FormView, generic.ListView):
    template_name = "jobs/job-detail.html"
    model = models.Job
    form_class = forms.RunJob
    command_name = None
    app_config_name = None
    context_object_name = "job_history"
    paginate_by = 10
    request: types.AuthenticatedRequest[User]

    class JobDetailHistoryTemplateSerializer(serializers.Serializer):
        pk = serializers.IntegerField()
        created_at = serializers.DateTimeField(format=None)
        created_by = serializers.CharField()
        cancelled_at = serializers.CharField()
        finished_at = serializers.CharField()
        started_at = serializers.CharField()
        has_finished = serializers.BooleanField()

    serializer_class = JobDetailHistoryTemplateSerializer

    def dispatch(self, request, *args, **kwargs):
        self.command_name = kwargs["command_name"]
        if not domain.can_access_job(self.command_name, self.request.user):
            raise exceptions.PermissionDenied
        try:
            self.app_config_name = domain.get_app_config_name(self.command_name)
        except management.CommandError:
            raise http.Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.model.objects.filter(
            name=self.command_name, app_config_name=self.app_config_name
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        file_contents, file_path = domain.get_command_file_contents(
            self.app_config_name, self.command_name
        )
        ctx["command_display_name"] = domain.get_command_display_name(self.command_name)
        ctx["app_config_category"] = domain.get_app_config_category(
            self.app_config_name
        )
        ctx["file_contents"] = file_contents
        ctx["file_path"] = file_path
        ctx["info_text"] = domain.get_command_info_text(self.command_name)
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["app_config_name"] = self.app_config_name
        kwargs["command_name"] = self.command_name
        return kwargs

    def form_valid(self, form) -> http.HttpResponse:
        cleaned_data = form.cleaned_data

        options = {}
        if soft_time_limit := cleaned_data.pop("soft_time_limit"):
            options["soft_time_limit"] = int(soft_time_limit.total_seconds())

        new_job = job_usecases.launch_job_with_arguments(
            command_name=str(self.command_name),
            creator=self.request.user,
            data=cleaned_data,
            **options,
        )

        success_url = urls.reverse("jobs:job-status", kwargs={"pk": new_job.id})
        return shortcuts.redirect(success_url)


class JobStatus(generic.DetailView, generic.FormView):
    form_class = forms.JobStatusActionForm
    template_name = "jobs/job-status.html"
    context_object_name = "job"

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.command_name = self.get_object().name
        if not domain.can_access_job(self.command_name, self.request.user):
            raise exceptions.PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs) -> models.Job:
        return shortcuts.get_object_or_404(models.Job, id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["command_display_name"] = domain.get_command_display_name(self.command_name)
        return ctx

    def form_valid(self, form):
        if form.cleaned_data["action"] == forms.JobStatusActionForm.ACTION_CANCEL:
            return self._cancel_job()
        elif (
            form.cleaned_data["action"]
            == forms.JobStatusActionForm.ACTION_DOWNLOAD_OUTPUT
        ):
            return self._download_output()
        raise exceptions.PermissionDenied

    def _cancel_job(self) -> http.HttpResponse:
        job = self.get_object()
        try:
            domain.cancel_job(job)
        except domain.UnableToCancelJob as e:
            messages.error(self.request, str(e))  # noqa: G200
        else:
            messages.success(
                self.request, "This job has been cancelled and it won't run."
            )
        success_url = urls.reverse("jobs:job-status", kwargs={"pk": job.id})
        return shortcuts.redirect(success_url)

    def _download_output(self):
        job = self.get_object()
        response = http.HttpResponse(
            job.output, content_type="application/text charset=utf-8"
        )
        response[
            "Content-Disposition"
        ] = f'attachment; filename="job-output-{job.pk}.txt"'
        return response


class JobOutput(generic.DetailView):
    template_name = "jobs/partials/job-output.html"
    context_object_name = "job"
    request: types.AuthenticatedRequest[User]

    def dispatch(self, request, *args, **kwargs) -> response.HttpResponseBase:
        self.kwargs = kwargs
        self.command_name = self.get_object().name
        if not domain.can_access_job(self.command_name, self.request.user):
            raise exceptions.PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs) -> models.Job:
        return shortcuts.get_object_or_404(models.Job, id=self.kwargs["pk"])
