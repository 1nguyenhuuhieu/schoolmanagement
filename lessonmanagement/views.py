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
    return render(request, 'index.html', context)


    
def lessondashboard(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)
    now = datetime.now()

    latest_lesson = Lesson.objects.filter(teacher=request.user.teacher.id)[:3]
    if now.month < 9:
        classyear_list = SubjectClassYear.objects.filter(teacher=request.user.teacher.id).filter(startdate__year = now.year - 1 )
    else:
        classyear_list = SubjectClassYear.objects.filter(teacher=request.user.teacher.id).filter(startdate__year = now.year)

        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now, 'latest_lesson': latest_lesson, 'classyear_list':classyear_list
    }
    return render(request, 'lessondashboard.html', context)

def lessons(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)
    now = datetime.now()
        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now
    }
    return render(request, 'lessons.html', context)



    