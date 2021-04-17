from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from datetime import datetime


def index(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)
    now = datetime.now()
        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now
    }
    return render(request, 'base.html', context)


    