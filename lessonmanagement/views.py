from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify
from django.http import Http404
from django.shortcuts import redirect

from django.db.models import Count

from django.contrib.auth.decorators import login_required


from django.core.files.storage import FileSystemStorage

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


@login_required
def profile(request):
    context = {}
    return render(request, 'profile.html', context)


@login_required
def teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(user__id = teacher_id)
        context = {'teacher': teacher}
        return render(request, 'teacher/teacher.html', context )
    except:
        raise Http404("Lesson does not exist")

@login_required
def index(request):
    teacher = request.user.teacher
    news = News.objects.order_by('-upload_time')[:5].annotate(Count('viewer'))
    countlesson = Lesson.objects.filter(teacher=teacher.id).count()
    context = {}

    if countlesson:
        context['countlesson'] = countlesson

    if news:
        context['news'] = news
    

    return render(request, 'index.html', context)


    
def lessondashboard(request):
    teacher = request.user.teacher
    #lấy tiết đã dạy hiện tại để tính thời lượng giảng dạy
    subject_classyear = SubjectClassyear.objects.filter(teacher=teacher.id, is_teach_now=True)
    context = { 'subject_classyear': subject_classyear
    }
    return render(request, 'lessondashboard.html', context)

def alllessons(request):
    lesson_list = Lesson.objects.filter(teacher=request.user.teacher.id)
    context = {'lesson_list': lesson_list}
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
        'lesson_list':lesson_list, 'classyear_list':classyear_list, 'subject':subject, 'level':level

    }
    return render(request, 'lessons.html', context)

def lesson_classyear(request, subject, level, title):

    context = { }
  
    return render(request, 'lessons_classyear.html', context)

def emptylesson(request):
    return render(request, 'no_lesson.html', {})

@login_required
def lesson(request, id):
    try:
        lesson = Lesson.objects.filter(teacher=request.user.teacher.id).get(id = id)
        return render(request, 'lesson/lesson.html', {'lesson': lesson})


    except Lesson.DoesNotExist:
        raise Http404("Lesson does not exist")
    
    
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

@login_required
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
            'subject_classyear': q1,
            'subject':subject,
            'level': level
        }
    except:
         return redirect('addlesson')

    if request.method == 'POST' and request.FILES['file_lesson']:
        title = request.POST['title_lesson']
        subject = request.POST['subject']
        subject_save = Subject.objects.get(subject_slug = subject)
        level_save = request.POST['level']
        start_lesson = request.POST['start_lesson']
        count_lesson = request.POST['count_lesson']
        description_lesson = request.POST['description_lesson']

        lesson = request.FILES['file_lesson']
        teacher_location = 'lessons/' + str(request.user.username)
        fs = FileSystemStorage(location=teacher_location)
        lesson_file =  fs.save(lesson.name, lesson)
        lesson_path =  teacher_location + '/' + fs.get_valid_name(lesson_file)

        new_lesson = Lesson(title=title, upload_time = now, level = level_save, description = description_lesson, teacher = request.user.teacher, subject = subject_save, start_number_lesson = start_lesson, cout_number_lesson = count_lesson, lesson_path = lesson_path  )
        new_lesson.save()



        

 
    return render(request, 'lesson/add_lesson_subject.html', context)
        



def lessons_toyear(request, year):
    context = {}

    return render(request, 'lesson/lesson_toyear.html', context)
