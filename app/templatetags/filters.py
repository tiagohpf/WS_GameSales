from django import template
from django.template.defaultfilters import stringfilter
from constants import *

baseEntity = "http://www.games.com/entity/"
baseProperty = "http://www.games.com/pred/"
register = template.Library()


@register.filter(name='format_string')
@stringfilter
def format_string(value):
    values = value.replace(baseEntity, '').replace(baseProperty, '').replace('_', ' ').split(' ')
    res = ""
    for i in values:
        if i in areas or i in platforms:
            res += i.upper() + ' '
        else:
            res += i.capitalize() + ' '
    return res.strip()