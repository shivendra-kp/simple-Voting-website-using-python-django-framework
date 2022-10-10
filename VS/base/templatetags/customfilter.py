from atexit import register
from django import template

register = template.Library()

@register.filter
def get_dict_value(d, key):
    return d[key]