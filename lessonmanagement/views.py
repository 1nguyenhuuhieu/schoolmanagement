from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify


now = datetime.now()
    
def index(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)
        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now
    }
    
    return render(request, 'index.html', context)


    
def lessondashboard(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)

        
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)

        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 
    }
    return render(request, 'lessondashboard.html', context)

def alllessons(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id).order_by('-upload_time')
    
    if now.month < 9:
        listyear = [now.year, now.year-1]
        lesson_toyear = Lesson.objects.filter(teacher=request.user.teacher.id).filter(upload_time__year__in=listyear)
        
    else:
        lesson_toyear = Lesson.objects.filter(teacher=request.user.teacher.id).filter(upload_time__year=now.year)
        

    lesson_pending = Lesson.objects.filter(teacher=request.user.teacher.id).filter(status="pending").order_by('-upload_time')
    lesson_acept = Lesson.objects.filter(teacher=request.user.teacher.id).filter(status="acept").order_by('-upload_time')
    lesson_deny = Lesson.objects.filter(teacher=request.user.teacher.id).filter(status="deny").order_by('-upload_time')
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)

        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now, 'lesson_pending':lesson_pending,'lesson_acept':lesson_acept, 'lesson_deny':lesson_deny,'lesson_toyear':lesson_toyear
    }
    return render(request, 'all_lessons.html', context)

def lessons_subject_level(request, subject, level):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id).filter(slug_subject = subject).filter(level = level)
    title = lesson.values_list('subject__title','level').distinct()
    context = {'lesson_list': lesson, 'title': title }
    return render(request, 'lessons.html', context)





    