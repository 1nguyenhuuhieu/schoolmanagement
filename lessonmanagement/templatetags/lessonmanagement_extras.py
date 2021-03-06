import datetime
from django import template
from lessonmanagement.models import Schoolyear
register = template.Library()


@register.filter
def classlevel(value):
    now = datetime.datetime.now()
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
    now = datetime.datetime.now()
    if (now.month < 9):
        return now.year -1
    else:
        return now.year


@register.filter
def plus_days(value, days):
    return value + datetime.timedelta(days=days)



@register.simple_tag
def now_schoolyear_tag():
    year =  Schoolyear.objects.get(
        is_active=True
    ).start_date.year

    return year