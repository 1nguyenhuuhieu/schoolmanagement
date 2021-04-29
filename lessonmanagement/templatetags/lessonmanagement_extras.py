from datetime import datetime
from django import template
register = template.Library()

@register.filter
def classlevel(value):
    now = datetime.now()
    i = 0
    if (now.month < 9):
        i =  (now.year - value) + 5
    else:
        i = (now.year - value) + 6
    if i in [6,7,8,9]:
        return i
    else:
        return value

@register.filter
def schoolyear(value):
    now = datetime.now()
    if (now.month < 9):
        return now.year -1
    else:
        return now.year