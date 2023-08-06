import argparse
import datetime
import shlex

from django import forms
from django.core import management

from commands_ui import models

# List of `dest` management command arguments to ignore and not render in the form.
IGNORED_ARGUMENT_NAMES = [
    "help",
    "version",
    "settings",
    "pythonpath",
    "traceback",
    "no_color",
    "force_color",
    "job_id",
    "verbosity",
    "configuration",
]


STORE_FALSE_HELP = (
    " - This is a `store_false` argument field. It means that if you uncheck this option, "
    "`{option_name}` will be passed as an argument to the management command."
)

User = models.get_user_model()


class RunJob(forms.Form):
    soft_time_limit = forms.DurationField(
        required=True,
        initial=datetime.timedelta(hours=1),
        help_text="End this task if it runs for longer than this. See: https://docs.celeryq.dev/en/stable/userguide/workers.html#time-limits",
    )

    def __init__(self, app_config_name, command_name, *args, **kwargs):
        self.app_config_name = app_config_name
        self.command_name = command_name
        super().__init__(*args, **kwargs)

        command = management.load_command_class(app_config_name, command_name)
        parser = command.create_parser(command_name, "")

        # Put all the management command arguments on a list, skipping the ignored ones.
        action_list = [
            action
            for action in parser._actions
            if action.dest not in IGNORED_ARGUMENT_NAMES
        ]

        # Add a field per store action
        for action in action_list:
            # If the string `file` is on the action dest, we'll assume it's a file.
            if "file" in action.dest.split("_") and action.type != str:
                field = forms.FileField(
                    required=False, label=action.dest, help_text=action.help
                )
            # If it has choices, display a choice field.
            elif action.choices:
                choices = [(str(c), str(c)) for c in action.choices]
                if not action.required:
                    # We need to manually add the empty choice if the field is not required
                    choices.insert(0, ("", "----------"))

                field = forms.ChoiceField(help_text=action.help, choices=choices)
            elif action.type == datetime.date:
                field = forms.CharField(
                    help_text=action.help,
                    widget=forms.TextInput(attrs={"data-field-type": "date"}),
                )
            elif action.type == datetime.datetime:
                field = forms.CharField(
                    help_text=action.help,
                    widget=forms.TextInput(attrs={"data-field-type": "date_time"}),
                )
            elif action.type == int:
                field = forms.IntegerField(help_text=action.help)
            # The way _StoreTrueAction and _StoreFalseAction args work is the following:
            # - if the user checks a _StoreTrueAction field in this form, the `option string` of
            # the argument should be passed to the management command.
            # - if the user does not check a _StoreFalseAction field in this form, the `option
            # string` of the argument should be passed to the management command.
            elif isinstance(action, argparse._StoreTrueAction):
                field = forms.BooleanField(help_text=action.help)
                field._store = True
            elif isinstance(action, argparse._StoreFalseAction):
                field = forms.BooleanField(
                    help_text=(
                        f"{action.help}"
                        f"{STORE_FALSE_HELP.format(option_name=action.option_strings[0])}"
                    ),
                )
                field._store = False
            # Otherwise, just render a text input.
            else:
                field = forms.CharField(help_text=action.help)
            try:
                field_name = action.option_strings[0]
            except IndexError:
                field_name = f"___{action.dest}"

            # Copy over some common properties from the source action
            field.label = action.dest
            field.required = action.required
            field.initial = action.default
            field.nargs = action.nargs

            assert (
                field_name not in self.fields
            ), f"{field_name} job argument clashes with form field; please rename {field_name}"

            self.fields[field_name] = field

    def clean(self):
        """
        Store the cleaned data in the same order the fields are displayed in the form.
        """
        submitted_data = super().clean()
        cleaned_data = {}

        for field_name, field in self.fields.items():
            value = submitted_data[field_name]
            # If the field is a boolean field, check if it's a StoreTrue or a StoreFalse
            # and set the value on cleaned_data depending on that.
            if hasattr(field, "_store"):
                if field._store is True:
                    cleaned_data[field_name] = value
                else:
                    cleaned_data[field_name] = not value
            elif not field.required and (value is None or value == ""):
                # Treat empty non-required fields as if they weren't there
                continue
            elif nargs := getattr(field, "nargs", None):
                cleaned_data[field_name] = _clean_nargs_value(nargs, value)
            else:
                cleaned_data[field_name] = value

        return cleaned_data


def _clean_nargs_value(nargs: str | int, value: str) -> str | list[str]:
    """
    Parse the value in a similar way to how argparse would handle nargs command-line arguments.

    '?' will gather all arguments into a single value. This is different to argparse, which
    would just take the first value. Because this value is submitted through a web form, we
    assume the user intended to pass a single value, e.g. "Good Energy" and not just "Good".
    '*', '+', or an integer will gather arguments into a list.
    """

    if nargs == "?":
        return value

    values = shlex.split(value)

    if isinstance(nargs, int):
        return values[:nargs]
    else:
        return values


class JobStatusActionForm(forms.Form):
    ACTION_CANCEL = "cancel"
    ACTION_DOWNLOAD_OUTPUT = "download-output"
    ACTION_CHOICES = (
        (ACTION_CANCEL, ACTION_CANCEL),
        (ACTION_DOWNLOAD_OUTPUT, ACTION_DOWNLOAD_OUTPUT),
    )
    action = forms.ChoiceField(choices=ACTION_CHOICES)


class JobFilterForm(forms.Form):
    """
    Form for filtering jobs.
    """

    created_by = forms.ChoiceField(required=False, initial="", choices=())

    job_name_search = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        created_by_choices = [
            ("", "All users"),
        ]
        for support_user in (
            User.objects.filter(job__isnull=False)
            .distinct()
            .order_by("first_name", "last_name")
        ):
            created_by_choices.append((support_user.id, support_user.get_full_name()))
        self.fields["created_by"].choices = created_by_choices
