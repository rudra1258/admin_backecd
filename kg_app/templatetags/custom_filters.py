from django import template

register = template.Library()

@register.filter
def nan_to_na(value):
    if str(value).lower() == 'nan':
        return 'NA'
    return value