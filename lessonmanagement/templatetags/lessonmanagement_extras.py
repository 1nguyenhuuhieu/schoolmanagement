import datetime
from django import template
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

@register.filter
# đổi từ tuần của năm dương lịch ra tuần của năm học
def schoolyear_week(value):
    now = datetime.datetime.now()
    if value > 34:
        return 'Tuần %s Học kì 1' % (str(value - 34))
    else:
        return 'Tuần %s Học kì 2' % (str(value - 1))

