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

    
   
    if now.month < 9:
        listyear = [now.year, now.year-1]
        lesson_toyear = Lesson.objects.filter(teacher=request.user.teacher.id).filter(upload_time__year__in=listyear)
        
    else:
        lesson_toyear = Lesson.objects.filter(teacher=request.user.teacher.id).filter(upload_time__year=now.year)
    lesson = lesson_toyear.filter(slug_subject = subject).filter(level = level)
    title = lesson.values_list('subject__title','level').distinct()
    title_class = lesson.order_by('classyear__title').values_list('classyear__title').distinct()
    
        

    lesson_pending = lesson.filter(status="pending").order_by('-upload_time')
    lesson_acept = lesson.filter(status="acept").order_by('-upload_time')
    lesson_deny = lesson.filter(status="deny").order_by('-upload_time')
    teachersubjectclassyear = lesson.filter(teacher=request.user.teacher.id)

        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear, 'now': now, 'lesson_pending':lesson_pending,'lesson_acept':lesson_acept, 'lesson_deny':lesson_deny,'lesson_toyear':lesson_toyear, 
    'title': title, 'title_class': title_class, 'subject':subject, 'level':level
    }
    return render(request, 'lessons.html', context)

def lesson_classyear(request, subject, level, title):
    subject2 = Lesson.objects.filter(slug_subject = subject).values_list('subject__title')
    subject_name = subject2[0][0]
    context = { 'level': level, 'subject_name': subject_name, 'subject_slug': subject, 'title': title}
  
    return render(request, 'lessons_classyear.html', context)

def emptylesson(request):
    return render(request, 'no_lesson.html', {})



    