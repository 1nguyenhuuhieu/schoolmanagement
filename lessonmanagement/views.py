from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User


def index(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    teachersubjectclassyear = SubjectClassYear.objects.filter(teacher=request.user.teacher.id)
    # lesson_classyear = Lesson.objects.filter(teacher=request.user.teacher.id)
    # print(lesson[1])

    for i in lesson:
        print (i.display_classyear())
        
    context = {'lesson_list':lesson,'teachersubjectclassyear':teachersubjectclassyear
    }
    return render(request, 'base.html', context)


    