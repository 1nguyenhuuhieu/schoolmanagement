from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.http import Http404


now = datetime.now()
    
def index(request):
    context = {
    }
    
    return render(request, 'index.html', context)


    
def lessondashboard(request):
    context = { 
    }
    return render(request, 'lessondashboard.html', context)

def alllessons(request):
    context = {}
    return render(request, 'all_lessons.html', context)

def lessons_subject_level(request, subject, level):
    lesson_list = LessonClassyear.objects.filter(subject_slug = subject).filter(classyear__startyear = level).filter(lesson__teacher = request.user.teacher.id)
    context = {
        'lesson_list':lesson_list

    }
    return render(request, 'lessons.html', context)

def lesson_classyear(request, subject, level, title):

    context = { }
  
    return render(request, 'lessons_classyear.html', context)

def emptylesson(request):
    return render(request, 'no_lesson.html', {})

def lesson(request, id):
    try:
        lesson = Lesson.objects.filter(teacher=request.user.teacher.id).get(id = id)

    except Lesson.DoesNotExist:
        raise Http404("Lesson does not exist")
    
    return render(request, 'lesson.html', {'lesson': lesson})

def addlesson(request):
    return render(request, 'lesson_add.html', {})
        


    