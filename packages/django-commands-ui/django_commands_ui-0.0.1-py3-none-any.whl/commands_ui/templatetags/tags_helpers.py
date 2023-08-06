from django import forms, template

register = template.Library()


@register.filter()
def title_case(value):
    value = value.replace("_", " ")
    return value.title()
