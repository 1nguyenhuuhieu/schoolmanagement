from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User


def index(request):
    lesson = Lesson.objects.filter(teacher=request.user.teacher.id)
    context = {'lesson_list': lesson}
    return render(request, 'base.html', context)


    