from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify
from django.http import Http404
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import *
from django.http import JsonResponse
import os

# đổi từ class level sang năm vào trường của một lớp
def level_to_startyear(level):
    now = datetime.datetime.now()
    if now.month < 9:
        return (now.year + 5 - level)
    else:
        return (now.year + 6 - level)


def class_level_def(year):
    now = datetime.datetime.now()
    i = 0
    if (now.month < 9):
        i = (now.year - year) + 5
    else:
        i = (now.year - year) + 6
    if i in [6, 7, 8, 9]:
        return i
    else:
        return year

# năm bắt đầu của niên khóa hiện tại
def current_schoolyear():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    if month > 9:
        return year
    else:
        return year - 1

# TRANG CHỦ
@login_required
def index(request):
    try:
        teacher = request.user.teacher
        news = News.objects.order_by(
            '-upload_time')[:5].annotate(Count('viewer'))
        countlesson = Lesson.objects.filter(teacher=teacher.id).count()
        page_title = 'Trang chủ'
        context = {'page_title': page_title}
        if countlesson:
            context['countlesson'] = countlesson
        if news:
            context['news'] = news
        return render(request, 'index.html', context)
    except:
        return redirect('create_profile')
# PROFILE
@login_required
def profile(request):
    list_subject = Subject.objects.values('title', 'id')
    if request.method == 'POST' and 'btnchangepassword' in request.POST:
        new_password = request.POST['new_password']
        current_user = User.objects.get(pk=request.user.id)
        current_user.set_password(new_password)
        current_user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Cập nhập thông tin thành công.')
        return redirect('profile', permanent=True)
    if request.method == 'POST' and 'changeprofile' in request.POST:
        current_user = Teacher.objects.get(user=request.user)
        fname = request.POST['fname']
        lname = request.POST['lname']
        birthdate = request.POST['birthdate']
        sex = request.POST['sex']
        number = request.POST['number']
        current_user.firstname = fname
        current_user.lastname = lname
        current_user.birth_date = birthdate
        current_user.zalo_number = number
        current_user.sex = sex
        current_user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Cập nhập thông tin thành công.')
        return redirect('profile', permanent=True)
    if request.method == 'POST' and 'btnchangeeducation' in request.POST:
        current_user = Teacher.objects.get(user=request.user)
        main_subject = request.POST['subject']
        education_level = request.POST['education']
        subject = Subject.objects.get(pk=main_subject)
        current_user.main_subject = subject
        current_user.education_level = education_level
        current_user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Cập nhập thông tin thành công.')
        return redirect('profile', permanent=True)
    if request.method == 'POST' and 'btnavatar' in request.POST and request.FILES['avatar']:
        current_user = Teacher.objects.get(user=request.user)
        lesson = request.FILES['avatar']
        teacher_location = 'media/avatar/' + str(request.user.username)
        lesson_location = teacher_location + '/'
        lesson_location_withoutmedia = 'avatar/' + \
            str(request.user.username) + '/'
        fs = FileSystemStorage(location=lesson_location)
        lesson_file = fs.save(lesson.name.replace(" ", "_"), lesson)
        lesson_path = lesson_location_withoutmedia + \
            fs.get_valid_name(lesson_file).replace(" ", "_")
        current_user.avatar = lesson_path
        current_user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Cập nhập thông tin thành công.')
        return redirect('profile', permanent=True)
    context = {'list_subject': list_subject,
               }
    return render(request, 'profile/profile.html', context)


@login_required
def teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(user__id=teacher_id)
        context = {'teacher': teacher}
        return render(request, 'teacher/teacher.html', context)
    except:
        raise Http404("Lesson does not exist")


@login_required
def lessondashboard(request):
    teacher = request.user.teacher
    # lấy tiết đã dạy hiện tại để tính thời lượng giảng dạy
    subject_classyear = SubjectClassyear.objects.filter(
        teacher=teacher.id, is_teach_now=True)
    context = {'subject_classyear': subject_classyear
               }
    return render(request, 'lessondashboard.html', context)


@login_required
def alllessons(request):
    lesson_list = Lesson.objects.filter(
        teacher=request.user.teacher.id).order_by('-upload_time')
    context = {'lesson_list': lesson_list}
    return render(request, 'all_lessons.html', context)


@login_required
def lessons_subject_level(request, subject, level):
    teacher = request.user.teacher.id
    schoolyear = current_schoolyear()
    now_school_year = Schoolyear.objects.get(start_date__year=schoolyear)
    # giáo án phù hợp với môn học và lớp học, giáo viên, niên khóa hiện tại
    lessons = Lesson.objects.filter(
        teacher=teacher, subject__subject__subject_slug=subject, subject__level=level, schoolyear=now_school_year)
    # sử dụng cho đường dẫn tới các lớp cụ thể
    classyear_list = SubjectClassyear.objects.filter(teacher=request.user.teacher.id).filter(
        subject__subject_slug=subject).filter(classyear__startyear=level_to_startyear(level))
    context = {
        'lesson_list': lessons, 'classyear_list': classyear_list, 'subject': subject, 'level': level
    }
    return render(request, 'lessons.html', context)

def lesson_classyear(request, subject, level, title):
    context = {}
    return render(request, 'lessons_classyear.html', context)

def emptylesson(request):
    return render(request, 'no_lesson.html', {})

@login_required
def lesson(request, id):
    try:
        lesson = Lesson.objects.filter(
            teacher=request.user.teacher.id).get(id=id)
        return render(request, 'lesson/lesson_detail.html', {'lesson': lesson})
    except Lesson.DoesNotExist:
        raise Http404("Lesson does not exist")

# Thêm giáo án tổng quan
@login_required
def addlesson(request):
    context = {}
    schoolyear = current_schoolyear()
    try:
        schoolyear = Schoolyear.objects.get(start_date__year=schoolyear)
    except:
        context = {
            'error': 'Không được phép thêm giáo án',
            'cause': 'Bạn chưa được phân công giảng dạy ở năm học ' + str(schoolyear) + ' - ' + str(schoolyear + 1),
        }
        return render(request, 'error/notfound.html', context)
    try:
        lesson_latest = Lesson.objects.filter(
            teacher=request.user.teacher.id).latest('upload_time')
        context['lesson_latest'] = lesson_latest
    except:
        context = {
        }
    return render(request, 'add_lesson.html', context)

# THÊM GIÁO ÁN VÀO SUBJECT VÀ LEVEL
@login_required
def add_lesson_subject_level(request, subject, level):
    context = {'subject': subject, 'level': level}
    now = datetime.datetime.now()
    teacher = request.user.teacher.id
    # lấy bài giảng đã thêm trong subject và level này
    q2 = Lesson.objects.filter(
        teacher=teacher, subject__subject__subject_slug=subject, subject__level=level)
    # kiểm tra phân công giảng dạy
    subjectclassyear = SubjectClassyear.objects.filter(
        teacher=teacher, subject__subject_slug=subject).values('classyear__startyear__start_date__year')
    subjectclassyear_list = []
    for i in subjectclassyear:
        class_level = class_level_def(
            i['classyear__startyear__start_date__year'])
        subjectclassyear_list.append(class_level)
    if level in subjectclassyear_list:
        try:
            latest_lesson = q2.latest('number_lesson')
            last_lesson = q2.all()[:5]
            context['last_lesson'] = last_lesson
            new_number_lesson = latest_lesson.number_lesson + 1
        except:
            new_number_lesson = 1
        context['new_number_lesson'] = new_number_lesson
        try:
            subject_title = Subject.objects.get(subject_slug=subject)
            context['subject_title'] = subject_title
            q_subject_level = SubjectLevel.objects.filter(
                subject__subject__subject_slug=subject, subject__level=level)
            if q_subject_level:
                current_title_lesson = q_subject_level.get(
                    number_lesson=new_number_lesson)
                new_title_lesson = list(SubjectLevel.objects.filter(
                    subject__subject__subject_slug=subject, subject__level=level).values('number_lesson', 'title'))
                context['new_title_lesson'] = new_title_lesson
                context['current_title_lesson'] = current_title_lesson
        except:
            return redirect('addlesson')
        if request.method == 'POST' and request.FILES['file_lesson']:
            title = request.POST['title_lesson']
            start_lesson = request.POST['start_lesson']
            description_lesson = request.POST['description_lesson']
            lesson = request.FILES['file_lesson']
            teacher_location = 'media/lessons/' + str(request.user.username)
            lesson_location = teacher_location + '/'
            lesson_location_withoutmedia = 'lessons/' + \
                str(request.user.username) + '/'
            fs = FileSystemStorage(location=lesson_location)
            lesson_file = fs.save(lesson.name.replace(" ", "_"), lesson)
            lesson_path = lesson_location_withoutmedia + \
                fs.get_valid_name(lesson_file).replace(" ", "_")
            year = Schoolyear.objects.get(
                start_date__year=current_schoolyear())
            q_subject = SubjectLesson.objects.get(
                subject__subject_slug=subject, level=level)
            print(q_subject)
            new_lesson = Lesson(title=title, upload_time=now, description=description_lesson, teacher=teacher,
                                subject=q_subject, number_lesson=start_lesson, lesson_path=lesson_path, schoolyear=year)
            new_lesson.save()
            messages.success(
                request, 'Vui lòng chờ giáo án của bạn được duyệt.')
            return redirect('lesson', id=new_lesson.id, permanent=True)
        return render(request, 'lesson/add_lesson_subject.html', context)
    else:
        return redirect('no_permisson_add_lesson')


@login_required
def no_permisson_add_lesson(request):
    context = {
        'error': 'Không tìm thấy phân công giảng dạy phù hợp',
        'cause': 'Bạn không được phân công giảng dạy lớp này',
    }
    return render(request, 'error/notfound.html', context)


@login_required
def edit_lesson(request, lesson_id):
    now = datetime.datetime.now()

    try:
        lesson = Lesson.objects.filter(
            teacher=request.user.teacher.id).get(id=lesson_id)
        context = {'lesson': lesson}
        if request.method == "POST":
            title = request.POST['title_lesson']
            start_lesson = request.POST['start_lesson']
            count_lesson = request.POST['count_lesson']
            description_lesson = request.POST['description_lesson']
            lesson.title = title
            lesson.start_number_lesson = start_lesson
            lesson.cout_number_lesson = count_lesson
            lesson.description = description_lesson
            lesson.status = 'pending'
            lesson.edit_time = now
            lesson.save()
            if bool(request.FILES.get('file_lesson', False)) == True:
                lesson_file_form = request.FILES['file_lesson']
                teacher_location = 'media/lessons/' + \
                    str(request.user.username)
                fs = FileSystemStorage(location=teacher_location)
                lesson_file = fs.save(lesson_file_form.name, lesson_file_form)
                lesson_path = teacher_location + '/' + \
                    fs.get_valid_name(lesson_file)
                lesson.lesson_path = lesson_path
                lesson.save()
            return redirect('lesson', id=lesson.id, permanent=True)
        return render(request, 'lesson/edit_lesson.html', context)
    except:
        raise Http404("fuck wrong")

def lessons_toyear(request, year):
    context = {}
    return render(request, 'lesson/lesson_toyear.html', context)

# lịch báo giảng
def schedule(request, year, week):
    now = datetime.datetime.now()
    now_school_year = current_schoolyear()
    # danh sách các niên khoá đã mở cho vào list
    schoolyear = Schoolyear.objects.dates('start_date', 'year')
    list_schoolyear = []
    for i in schoolyear:
        list_schoolyear.append(i.year)
    # năm trong URL có thoả mãn niên khoá đã mở
    if year in list_schoolyear or (year-1) in list_schoolyear:
        # lấy giáo án thuộc năm học <year> tương ứng với <week>
        naive_schoolyear = 0
        # tuần hiện tại là < tháng 9
        if week < 36:
            naive_schoolyear = year - 1
        else:
            naive_schoolyear = year
        lessons = LessonClassyear.objects.filter(
            lesson__teacher=request.user.teacher.id, lesson__schoolyear__start_date__year=naive_schoolyear)
        # lịch báo giảng của tuần thứ <week> và năm <naive_schoolyear> lấy theo URL
        schedule_all = lessons.filter(week=week)
        schedule_morning = schedule_all.filter(session='morning')
        schedule_afternoon = schedule_all.filter(session='afternoon')
        # lấy ngày thứ hai của năm <year> và tuần <week> from URL
        d = '%s-W%s' % (year, week)
        monday = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
        context = {
            'now_school_year': now_school_year,
            'week': week,
            'year': year,
            'schedule_morning': schedule_morning,
            'schedule_afternoon': schedule_afternoon,
            'monday': monday,
        }
        return render(request, 'schedule/schedule.html', context)
    else:
        return redirect('emptyschedule')

# không tìm thấy lịch báo giảng với năm học đã cho từ URL
def emptyschedule(request):
    context = {
        'error': 'Không tìm thấy lịch báo giảng phù hợp',
        'cause': 'Năm học này không tồn tại trên hệ thống',
    }
    return render(request, 'error/notfound.html', context)

# thêm giáo án vào lịch báo giảng
@login_required
def add_lesson_schedule(request, lesson_id):
    if request.method == "POST":
        classyear_form = request.POST['classyear']
        classyear = Classyear.objects.get(id=classyear_form)
        schedule_date = request.POST['schedule_date']
        session_schedule = request.POST['session']
        order_schedule = request.POST['order']
        new_schedule = LessonClassyear(is_teach=False, lesson=lesson, classyear=classyear, session=session_schedule, order_schedule=order_schedule, teach_date_schedule=schedule_date)
        new_schedule.save()
        q = LessonClassyear.objects.get(pk=new_schedule.id)
        week = q.teach_date_schedule.isocalendar()[1]
        new_schedule.week = week
        new_schedule.save()
        messages.success(request, 'Lịch báo giảng đã được thêm.')
        if 'quit' in request.POST:
            return redirect('lesson', id=lesson_id, permanent=True)
        if 'continue' in request.POST:
            return redirect('add_lesson_schedule', lesson_id=lesson_id, permanent=True)
    context = {}
    return render(request, 'schedule/add_lesson_schedule.html', context)

@login_required
def manager(request):
    try:
        currentuser = SubjectTeacher.objects.filter(
            teacher=request.user.id, role='manager').values('subject')
        member = SubjectTeacher.objects.filter(subject__id__in=currentuser)
        context = {'member': member}
        return render(request, 'manager/manager.html', context)
    except:
        raise Http404('d')
