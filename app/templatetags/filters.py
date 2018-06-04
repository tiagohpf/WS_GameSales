from django import template
from django.template.defaultfilters import stringfilter
from constants import *

baseEntity = "http://www.games.com/entity/"
baseProperty = "http://www.games.com/pred/"
register = template.Library()


@register.filter(name='format_string')
@stringfilter
def format_string(value):
    value = value.replace(baseEntity, '').replace(baseProperty, '').replace('_', ' ')
    if ' ' in value:
        value = split_by_space(value)
    if '/' in value:
        value = split_by_bar(value)
    if '-' in value:
        value = split_by_hyphen(value)
    if ' ' not in value and '/' not in value and '-' not in value:
        value = value.title()
    return value


def split_by_space(value):
    if ' ' in value:
        words = value.split(' ')
        res = ""
        for word in words:
            if word in areas or word in platforms:
                res += word.upper() + ' '
            else:
                res += word.title() + ' '
        return res.strip()
    return value


def split_by_bar(value):
    words = value.split('/')
    res = ""
    for word in words:
        if word in areas or word in platforms:
            res += word.upper() + '/'
        else:
            res += word.title() + '/'
    return res[:-1].strip()


def split_by_hyphen(value):
    words = value.split('-')
    res = ""
    for word in words:
        if word in areas or word in platforms:
            res += word.upper() + '-'
        else:
            res += word.title() + '-'
    return res[:-1].strip()
