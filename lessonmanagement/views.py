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
    
    #id của những giáo án phù hợp với môn học và lớp học, giáo viên
    lesson_id_list_dict = list(LessonClassyear.objects.filter(lesson__subject__subject_slug = subject).filter(classyear__startyear = level).filter(lesson__teacher = request.user.teacher.id).values('lesson__id').distinct())

    #sử dụng cho đường dẫn tới các lớp cụ thể
    classyear_list = LessonClassyear.objects.filter(lesson__subject__subject_slug = subject).filter(classyear__startyear = level).filter(lesson__teacher = request.user.teacher.id).values('classyear__title').distinct()

    lesson_id_list = []
    for i in lesson_id_list_dict:
        lesson_id_list.append(i['lesson__id'])
    
    #danh sách giáo án với subject và startyear tương ứng
    lesson_list = Lesson.objects.filter(id__in = lesson_id_list)
    context = {
        'lesson_list':lesson_list, 'classyear_list':classyear_list

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
        


    