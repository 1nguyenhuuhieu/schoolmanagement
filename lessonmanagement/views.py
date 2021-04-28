from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.http import Http404
from django.shortcuts import redirect


now = datetime.now()


#đổi từ class level sang năm vào trường của một lớp
def level_to_startyear(level):
    if now.month < 9:
        return (now.year + 5 - level)
    else:
        return (now.year + 6 - level)

def class_level_def(year):
    i = 0
    if (now.month < 9):
        i =  (now.year - year) + 5
    else:
        i = (now.year - year) + 6
    if i in [6,7,8,9]:
        return i
    else:
        return year


def index(request):
    context = {
    }
    
    return render(request, 'index.html', context)


    
def lessondashboard(request):
    teacher = request.user.teacher
    #lấy tiết đã dạy hiện tại để tính thời lượng giảng dạy
    subject_classyear = SubjectClassyear.objects.filter(teacher=teacher.id, is_teach_now=True)
    context = { 'subject_classyear': subject_classyear
    }
    return render(request, 'lessondashboard.html', context)

def alllessons(request):
    teacher = request.user.teacher
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

    try:
        lesson_latest = Lesson.objects.filter(teacher=request.user.teacher.id).latest('upload_time')
        context = { 
            'lesson_latest': lesson_latest
        }
    except:
        context = { 
        }

    return render(request, 'add_lesson.html', context)

def add_lesson_subject_level(request, subject, level):
    teacher = request.user.teacher.id
    q2 = Lesson.objects.filter(teacher=teacher).filter(subject__subject_slug = subject).filter(level = level)
    try:
        latest_lesson = q2.latest('start_number_lesson')
        new_number_lesson = latest_lesson.start_number_lesson + latest_lesson.cout_number_lesson
    except:
        new_number_lesson = 1
      
    try:

        q1 = SubjectClassyear.objects.filter(teacher = teacher).filter(subject__subject_slug=subject).filter(classyear__startyear = level_to_startyear(level))
        subject_classyear_list = q1.latest('id')

        subject_level_title = subject_classyear_list.subject.title + ' ' + str(level)
        classyear_title_list = ', '.join(str(class_level_def(i.classyear.startyear)) + i.classyear.title for i in q1)

        last_lesson = q2.order_by('-upload_time')[:5]
       
        context = {
            'subject_classyear_list': subject_classyear_list,
            'subject_level_title': subject_level_title,
            'new_number_lesson': new_number_lesson,
            'classyear_title_list': classyear_title_list,
            'last_lesson': last_lesson,
            'subject_classyear': q1
        }
    except:
         return redirect('addlesson')

 
    return render(request, 'add_lesson_subject_level.html', context)
        


    