from django import contrib
from django import shortcuts
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
import datetime
from django.utils.text import normalize_newlines, slugify
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
from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models import Q


# đổi từ class level sang năm vào trường của một lớp
def level_to_startyear(level):
    now = datetime.datetime.now()
    if now.month < 8:
        return (now.year + 5 - level)
    else:
        return (now.year + 6 - level)

def class_level_def(year):
    now = datetime.datetime.now()
    i = 0
    if (now.month < 8):
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
    if month > 8:
        return year
    else:
        return year - 1

# lấy object Schoolyear của năm hiện tại
def q_schoolyear():
    return Schoolyear.objects.get(is_active=True)

# đổi ngày hiện tại sang tuần tương ứng của năm học
def now_week_schoolyear(schoolyear):
    start_day = schoolyear.start_date
    start_monday = start_day + datetime.timedelta(days=-start_day.weekday())
    today = datetime.date.today()
    week = (today - start_monday)/7
    return week.days

# đổi ngày bất kì sang tuần tương ứng của năm học
def day_week_schoolyear(schoolyear, d):
    start_day = schoolyear.start_date
    start_monday = start_day + datetime.timedelta(days=-start_day.weekday())
    week = (d - start_monday)/7
    return week.days

# lấy ngày thứ hai của tuần năm học
def monday_week_schoolyear(schoolyear, week):
    start_day = schoolyear.start_date
    start_monday = start_day + datetime.timedelta(days=-start_day.weekday())
    now_monday = start_monday + datetime.timedelta(days = week*7)
    return now_monday

# TRANG CHỦ
@login_required
def index(request):
    page_title = 'Trang chủ'
    school = get_object_or_404(School, pk=1)
    schoolyear = q_schoolyear()
    week = now_week_schoolyear(schoolyear)
    monday = monday_week_schoolyear(schoolyear, week)
    context = {
        'page_title': page_title,
        'schoolyear': schoolyear,
        'week': week,
        'monday': monday,
        'school': school,
    }
    return render(request, 'index.html', context)

# PROFILE
@login_required
def profile(request):
    list_subject = Subject.objects.values('title', 'id')
    if request.method == 'POST' and 'btnchangepassword' in request.POST:
        new_password = request.POST['new_password']
        current_user = User.objects.get(pk=request.user.id)
        current_user.set_password(new_password)
        current_user.save()
        messages.add_message(request, messages.SUCCESS, 'Cập nhập thông tin thành công.')
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
    context = {
        'list_subject': list_subject,
        'page_title': "Thông tin cá nhân",

    }
    return render(request, 'profile/profile.html', context)

@login_required
def profile_detail(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    subjects = SubjectManager.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear(), is_active=True
    )
    context = {
        'teacher_context': teacher,
        'subjects': subjects
    }
    return render(request, 'profile/profile_detail.html', context)

@login_required
def teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(user__id=teacher_id)
        context = {'teacher': teacher}
        return render(request, 'teacher/teacher.html', context)
    except:
        raise Http404("Lesson does not exist")

# THƯ VIỆN GIÁO ÁN
@login_required
def lessons(request, schoolyear):
    teacher = request.user.teacher.id
    schoolyears = Schoolyear.objects.filter(
        subjectclassyear__teacher=teacher
    ).distinct()
    if schoolyear == 0:
        q_schoolyear = schoolyears
        lessons = Lesson.objects.filter(
        teacher=teacher, schoolyear__in=q_schoolyear
        ).order_by('-upload_time')
        page_title = "Thư viện giáo án"
    else:
        q_schoolyear = schoolyears.get(
            start_date__year=schoolyear
            )
        lessons = Lesson.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear
        ).order_by('-upload_time')
        page_title = 'Giáo án năm'

    context = {
        'current_year': q_schoolyear,
        'lesson_list': lessons,
        'schoolyear': schoolyears,
        'page_title': page_title
    }
    return render(request, 'lesson/lessons.html', context)

@login_required
def lessons_subject(request, subject):
    teacher = request.user.teacher.id
    schoolyear = q_schoolyear()
    # giáo án phù hợp với môn học và lớp học, giáo viên, niên khóa hiện tại
    lessons = Lesson.objects.filter(
        teacher=teacher, subject__slug=subject, schoolyear=schoolyear
        )
    context = {
        'lesson_list': lessons,
        'subject': subject
    }
    return render(request, 'lesson/lessons_subject.html', context)

def lesson_classyear(request, subject, level, title):
    context = {}
    return render(request, 'lesson/lessons_classyear.html', context)

def emptylesson(request):
    return render(request, 'lesson/no_lesson.html', {})

@login_required
def lesson(request, id):
    teacher = request.user.teacher.id
    lesson = get_object_or_404(Lesson,teacher=teacher, pk=id )
    if request.method == "POST" and "delete" in request.POST:
        schedule_id = request.POST['schedule_id']
        schedule = LessonSchedule.objects.get(pk=schedule_id)
        schedule.delete()
        messages.success(request, 'Lịch báo giảng đã được xóa thành công.')
        return redirect('lesson',id=id, permanent=True)
    context = {
        'lesson': lesson,
        'page_title': lesson.title
    }
    return render(request, 'lesson/lesson_detail.html', context)


@login_required
def week_lessons(request, subject, level):
    teacher = request.user.teacher.id
    schoolyear = q_schoolyear()
    week = now_week_schoolyear(schoolyear)
    subjects = SubjectClassyear.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear()
    )
    lessons = Lesson.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear(), week=week)
    if subject != 'all':
        lessons = lessons.filter(
            subject__subject__subject_slug=subject, subject__level=level
        )
        subject_title = Subject.objects.get(subject_slug=subject)
        subject_level = level
    else:
        subject_title = 'Tất cả'
        subject_level = ''
    context = {
        'lesson_list': lessons,
        'subjects': subjects,
        'subject_title': subject_title,
        'subject_level': subject_level,
        'week': week,
        'page_title': 'Giáo án tuần này'
    }
    return render(request, 'lesson/week_lessons.html', context)

@login_required
def open_lesson(request, id):
    teacher = request.user.teacher.id
    lesson = Lesson.objects.get(
        pk=id, teacher=teacher
    )
    context = {
        'lesson': lesson,
        'page_title': lesson.title
    }

    return render(request,'lesson/open_lesson.html',context)

# Thêm giáo án tổng quan
@login_required
def addlesson(request):
    now = datetime.datetime.now()
    now_week = now.isocalendar()[1]
    teacher = request.user.teacher.id
    schoolyear = q_schoolyear()
    #tuần tiếp theo của tuần hiện tại
    week = now_week_schoolyear(schoolyear) + 1
    subjectclassyear = SubjectClassyear.objects.filter(
        teacher=teacher, schoolyear=schoolyear
    )
    
    subjectclassyear_count = subjectclassyear.filter(
        subject__lesson__schoolyear=schoolyear, subject__lesson__teacher=teacher
    ).annotate(models.Count('subject__lesson'))

    subjectclassyear_week_count = subjectclassyear.filter(
        subject__lesson__schoolyear=schoolyear, subject__lesson__upload_time__week=now_week, subject__lesson__teacher=teacher
    ).annotate(models.Count('subject__lesson'))

    subjectclassyear_week = subjectclassyear.filter(
        subject__lesson__schoolyear=schoolyear, subject__lesson__upload_time__week=now_week, subject__lesson__teacher=teacher
    )
    
    empty_week = subjectclassyear.difference(subjectclassyear_week)

    context = {
        'subjectclassyear': subjectclassyear,
        'subjectclassyear_count': subjectclassyear_count,
        'subjectclassyear_week_count': subjectclassyear_week_count,
        'empty_week': empty_week,
        'page_title': 'Thêm giáo án',
        'week': week
    }
    return render(request, 'lesson/add_lesson.html', context)

# THÊM GIÁO ÁN VÀO SUBJECT VÀ LEVEL
@login_required
def add_lesson_subject_level(request, subject, level):
    schoolyear = q_schoolyear()
    #tuần tiếp theo của tuần hiện tại
    week = now_week_schoolyear(schoolyear) + 1
    monday = monday_week_schoolyear(schoolyear, week)
    now = datetime.datetime.now()
    teacher = request.user.teacher.id
    # kiểm tra phân công giảng dạy
    subjectclassyear = get_object_or_404(SubjectClassyear,
    teacher=teacher, subject__subject__subject_slug=subject, subject__level=level, schoolyear=schoolyear
    )
    # lấy bài giảng đã thêm trong subject và level này
    q2 = Lesson.objects.filter(
        teacher=teacher, subject=subjectclassyear.subject, schoolyear=schoolyear
    )
    last_lesson = q2.filter(
        week=week
    )[:5]
    #kiểm tra số giáo án tải lên tuần này
    lessons_week_count = Lesson.objects.filter(
        subject=subjectclassyear.subject, week=week, schoolyear=schoolyear
    ).count()
    subject_title = subjectclassyear.subject.subject.title
    is_add = True if lessons_week_count < subjectclassyear.subject.week_lesson else False
    context = {
        'subject': subject,
        'level': level,
        'schoolyear': schoolyear,
        'week': week,
        'monday': monday,
        'lessons_week_count': lessons_week_count,
        'subjectclassyear': subjectclassyear,
        'subject_title': subject_title,
        'is_add': is_add,
        'last_lesson': last_lesson,
        'page_title': "Thêm giáo án %s" % (subjectclassyear.subject)
        }
    # lấy số bài giảng của giáo án gần nhất để thêm vào default input HTML Template
    if is_add:
        if q2:
            latest_lesson = q2.latest('number_lesson')
            new_number_lesson = latest_lesson.number_lesson + 1
        else:
            new_number_lesson = 1
        context['new_number_lesson'] = new_number_lesson
        q_subject_level = SubjectLesson.objects.filter(subject__subject__subject_slug=subject, subject__level=level)
        try:  
            current_title_lesson = q_subject_level.get(number_lesson=new_number_lesson)
            new_title_lesson = list(SubjectLesson.objects.filter(subject__subject__subject_slug=subject, subject__level=level).values('number_lesson', 'title'))
            context['new_title_lesson'] = new_title_lesson
            context['current_title_lesson'] = current_title_lesson
        except:
            pass
        if request.method == 'POST' and request.FILES['file_lesson']:
            title = request.POST['title_lesson']
            start_lesson = request.POST['start_lesson']
            description_lesson = request.POST['description_lesson']
            lesson = request.FILES['file_lesson']
            teacher_location = 'media/lessons/' + str(request.user.username)
            lesson_location = teacher_location + '/'
            lesson_location_withoutmedia = 'lessons/' + str(request.user.username) + '/'
            fs = FileSystemStorage(location=lesson_location)
            lesson_file = fs.save(lesson.name.replace(" ", "_"), lesson)
            lesson_path = lesson_location_withoutmedia + fs.get_valid_name(lesson_file).replace(" ", "_")
            q_subject = subjectclassyear.subject
            new_lesson = Lesson(title=title, upload_time=now, description=description_lesson, teacher=request.user.teacher,subject=q_subject, number_lesson=start_lesson, lesson_path=lesson_path, schoolyear=schoolyear, week=week)
            new_lesson.save()
            messages.success(request, 'Vui lòng chờ giáo án của bạn được duyệt.')
            if 'add' in request.POST:
                return redirect('lesson', id=new_lesson.id, permanent=True)
            if 'continue' in request.POST:
                return redirect('add_lesson_subject_level', subject, level)
    return render(request, 'lesson/add_lesson_subject.html', context)

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
    teacher = request.user.teacher.id
    lesson = get_object_or_404(Lesson,
    teacher=teacher, pk=lesson_id, status="deny")
    context = {
        'lesson': lesson,
        'page_title': 'Sửa giáo án'}
    if request.method == "POST":
        title = request.POST['title_lesson']
        start_lesson = request.POST['start_lesson']
        description_lesson = request.POST['description_lesson']
        lesson.title = title
        lesson.number_lesson = start_lesson
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

# lịch báo giảng của năm học hiện tại
def schedule(request, username_url, year, week):
    username = request.user.username
    teacher = Teacher.objects.get(
        is_work=True, user__username=username_url
    )
    is_change = False
    if username == username_url:
        is_change = True
    if week <= 40:
        all_schoolyear = Schoolyear.objects.all()
        # năm học theo year
        schoolyear = Schoolyear.objects.get(start_date__year=year)
        now_week = now_week_schoolyear(schoolyear)
        if week == 0:
            week = now_week
        lessons = LessonSchedule.objects.filter(
            lesson__teacher=teacher, lesson__schoolyear=schoolyear
            )
        # lịch báo giảng của tuần thứ <week> và năm <schoolyear> lấy theo URL
        schedule_all = lessons.filter(week=week)
        schedule_morning = schedule_all.filter(session='morning')
        schedule_afternoon = schedule_all.filter(session='afternoon')
        # lấy ngày thứ hai của năm <schoolyear> và tuần <week> from URL
        monday = monday_week_schoolyear(schoolyear, week)
        #dữ liệu để thêm vào lịch báo giảng
        all_lesson = Lesson.objects.filter(
            teacher=teacher, schoolyear=schoolyear
            ).order_by(
                'subject__subjectclassyear__classyear'
                ).values(
                    'subject__subjectclassyear__classyear','subject__subjectclassyear__classyear__startyear__start_date__year','subject__subjectclassyear__classyear__title','id',  'subject__subject__title', 'subject__level','title').distinct()
        classyear = SubjectClassyear.objects.filter(
            teacher=teacher, schoolyear=schoolyear
            ).order_by(
                'classyear__startyear__start_date__year'
                ).values(
                    'classyear__startyear__start_date__year','classyear__title','classyear__id'
                    ).distinct()
      
        # dùng cho tìm kiếm theo tuần
        lessons_week = LessonSchedule.objects.filter(
            lesson__teacher = teacher, lesson__schoolyear=schoolyear
        ).dates('teach_date_schedule', 'week')
        lessons_week_schoolyear = []
        week_dict = {}
        monday_dict = {}
        for i in lessons_week:
            week_dict['week'] = day_week_schoolyear(schoolyear,i)
            monday_dict['monday'] = i
            lessons_week_schoolyear.append((week_dict, monday_dict))
            week_dict = {}
            monday_dict = {}

        if request.method == "POST" and 'add_schedule' in request.POST:
            date = request.POST['schedule_date']
            session = request.POST['session_date']
            order_schedule = request.POST['order_schedule']
            classyear_id = request.POST['classyear']
            classyear = Classyear.objects.get(pk=classyear_id)
            lesson_id = request.POST['lesson_id']
            lesson = Lesson.objects.get(pk=lesson_id)
            new_schedule = LessonSchedule(
                lesson=lesson, classyear=classyear, teach_date_schedule=date, session=session, order_schedule=order_schedule )
            new_schedule.save()
            q = LessonSchedule.objects.get(pk=new_schedule.id)
            d = q.teach_date_schedule
            d_week = day_week_schoolyear(schoolyear, d)
            q.week = d_week
            q.save()
            messages.success(request, 'Lịch báo giảng đã được thêm.')
            return redirect('schedule',username_url=username,year=year, week=week ,permanent=True)
        context = {
            'week': week,
            'year': year,
            'schedule_morning': schedule_morning,
            'schedule_afternoon': schedule_afternoon,
            'monday': monday,
            'all_lesson': all_lesson,
            'classyear': classyear,
            'lessons_week': lessons_week_schoolyear,
            'schoolyear': schoolyear,
            'now_week': now_week,
            'all_schoolyear': all_schoolyear,
            'username': username,
            'is_change': is_change,
            'username_url': username_url
        }
        if request.method == "GET" and 'btn_search_date' in request.GET:
            search_date = request.GET['search_date']
            date_search = datetime.datetime.strptime(search_date, '%Y-%m-%d')
            if date_search.month < 9:
                year = date_search.year - 1
            else:
                year = date_search.year
            date_search = date_search.date()
            schoolyear = Schoolyear.objects.get(start_date__year=year)
            week = day_week_schoolyear(schoolyear, date_search)
            return redirect('schedule',username_url=username, year=year, week=week, permanent=True)

        if request.method == "GET" and 'week_search' in request.GET:
            week_search = request.GET['week_search']
            year_week = request.GET['year_week']
            return redirect('schedule',username_url=username, year=year_week, week=week_search, permanent=True)
        return render(request, 'schedule/schedule.html', context)
    else:
        raise Http404
# không tìm thấy lịch báo giảng với năm học đã cho từ URL
def emptyschedule(request):
    context = {
        'error': 'Không tìm thấy lịch báo giảng phù hợp',
        'cause': 'Năm học này không tồn tại trên hệ thống',
    }
    return render(request, 'error/notfound.html', context)

#thêm giáo án vào ngày trong lịch báo giảng
@login_required
def add_schedule(request):
    teacher = request.user.teacher.id

    last_schedule = LessonSchedule.objects.filter(
        lesson__teacher=teacher
    ).order_by('-id')[:5]
    lessons = Lesson.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear()
    )
    classyear = SubjectClassyear.objects.filter(
            teacher=teacher, schoolyear=q_schoolyear()
            ).order_by(
                'classyear__startyear__start_date__year'
                ).values(
                    'classyear__startyear__start_date__year','classyear__title','classyear__id'
                    ).distinct()
    if request.method == "POST":
        classyear_id = request.POST['input_classyear']
        classyear = Classyear.objects.get(pk=classyear_id)
        schedule_date = request.POST['schedule_date']
        session_schedule = request.POST['session']
        order_schedule = request.POST['order']
        lesson_id = request.POST['lesson']
        lesson = Lesson.objects.get(pk=lesson_id)
        new_schedule = LessonSchedule(lesson=lesson, classyear=classyear, session=session_schedule, order_schedule=order_schedule, teach_date_schedule=schedule_date)
        new_schedule.save()

        q = LessonSchedule.objects.get(pk=new_schedule.id)
        schoolyear = lesson.schoolyear
        d = q.teach_date_schedule
        d_week = day_week_schoolyear(schoolyear, d)
        q.week = d_week
        q.save()
        messages.success(request, 'Lịch báo giảng đã được thêm.')
        if 'quit' in request.POST:
            return redirect('add_schedule', permanent=True)

        if 'continue' in request.POST:
            return redirect('add_schedule', permanent=True)
    context = {
        'last_schedule': last_schedule,
        'lessons': lessons,
        'classyear': classyear

    }
    return render(request, 'schedule/add_schedule.html', context)

# thêm giáo án vào lịch báo giảng
@login_required
def add_lesson_schedule(request, lesson_id):
    teacher = request.user.teacher.id
    lesson = Lesson.objects.get(teacher=teacher, pk=lesson_id)
    classyear_list = SubjectClassyear.objects.filter(
        teacher=teacher, schoolyear=q_schoolyear(), subject=lesson.subject
    ).values('classyear__id', 'classyear__title', 'classyear__startyear__start_date__year')
    schedule_list = LessonSchedule.objects.filter(lesson=lesson)
    if request.method == "POST":
        classyear_form = request.POST['input_classyear']
        classyear = Classyear.objects.get(id=classyear_form)
        schedule_date = request.POST['schedule_date']
        session_schedule = request.POST['session']
        order_schedule = request.POST['order']
        new_schedule = LessonSchedule(lesson=lesson, classyear=classyear, session=session_schedule, order_schedule=order_schedule, teach_date_schedule=schedule_date)
        new_schedule.save()
        q = LessonSchedule.objects.get(pk=new_schedule.id)

        schoolyear = lesson.schoolyear
        d = q.teach_date_schedule
        d_week = day_week_schoolyear(schoolyear, d)
        q.week = d_week
        q.save()
        messages.success(request, 'Lịch báo giảng đã được thêm.')
        if 'quit' in request.POST:
            return redirect('lesson', id=lesson_id, permanent=True)
        if 'continue' in request.POST:
            return redirect('add_lesson_schedule', lesson_id=lesson_id, permanent=True)
    context = {
        'lesson': lesson,
        'classyear_list': classyear_list,
        'schedule_list': schedule_list
    }
    return render(request, 'schedule/add_lesson_schedule.html', context)

@login_required
def guide(request):
    context = {

    }
    return render(request, 'guide/guide.html', context)


# DUYỆT GIÁO ÁN
@login_required
def check_lessons_subject(request, year, subject):
    checker = request.user.teacher.id
    schoolyear = Schoolyear.objects.get(start_date__year=year)
    subjects = SubjectManager.objects.filter(
        teacher=checker, schoolyear=schoolyear
    )
    if subject == 'all':
        subject_title = 'Tất cả môn học'
        lessons = Lesson.objects.filter(
            schoolyear=schoolyear, subject__subject__subjectmanager__teacher=checker, subject__subject__subjectmanager__is_active=True
        )
    else:
        subject_title = Subject.objects.get(subject_slug=subject)
        lessons = Lesson.objects.filter(
            schoolyear=schoolyear, subject__subject__subjectmanager__teacher=checker, subject__subject__subjectmanager__is_active=True, subject__subject__subject_slug=subject
        )
    lessons_pending = lessons.filter(
        status='pending'
    )
    lessons_acept = lessons.filter(
        status='acept'
    )
    lessons_deny = lessons.filter(
        status='deny'
    )
    context = {
        'lesson_list': lessons,
        'lessons_pending': lessons_pending,
        'lessons_acept': lessons_acept,
        'lessons_deny': lessons_deny,
        'subjects': subjects,
        'subject': subject_title,
        'year': year
    }
    return render(request, 'lesson/check_lessons.html', context)

@login_required
def check_lesson(request,lesson_id):
    teacher = request.user.teacher.id
    lesson = Lesson.objects.get(
        pk=lesson_id
    )
    subject = lesson.subject.subject
    schoolyear = lesson.schoolyear
    subjectmanager = SubjectManager.objects.filter(
        teacher=teacher, subject=subject, schoolyear=schoolyear 
    )
    if subjectmanager:
        context = {
            'lesson': lesson
        }
        return render(request, 'lesson/check_lesson.html', context)
    else:
        raise Http404

@login_required
def check_open_lesson(request, lesson_id):
    checker = request.user.teacher.id
    lesson = get_object_or_404(Lesson,
    pk=lesson_id, subject__subject__subjectmanager__teacher=checker
        )
    if request.method == "POST" and 'btn_change_status' in request.POST:
        status = request.POST['status']
        note = request.POST['note']
        lesson.status = status
        lesson.checker = request.user.teacher
        lesson.note_checker = note
        lesson.save()
        messages.add_message(request, messages.SUCCESS, 'Cập nhập trạng thái giáo án thành công.')
        return redirect('check_open_lesson', lesson_id, permanent=True)

    context = {
        'lesson': lesson
    }
    return render(request, 'lesson/open_lesson_check.html', context)


@login_required
def dashboard(request):
    teacher_manager = request.user.teacher.id
    manager = get_object_or_404(
        SchoolManager, is_active=True, schoolyear=q_schoolyear(), teacher=teacher_manager
    )
    teachers = Teacher.objects.filter(
        is_work=True
    )

    complete_teacher_lesson = teachers
    incomplete_teacher_lesson = teachers


    for teacher in complete_teacher_lesson:
        if not teacher.is_complete_subjectclassyear():
            complete_teacher_lesson = complete_teacher_lesson.exclude(pk=teacher.id)
        else:
            incomplete_teacher_lesson = incomplete_teacher_lesson.exclude(pk=teacher.id)



    #giáo án đã gửi lên tuần hiện tại
    context = {
        'teachers': teachers,
        'complete_teacher_lesson': complete_teacher_lesson,
        'incomplete_teacher_lesson': incomplete_teacher_lesson,
        
    }

    return render(request, 'dashboard/home.html', context)
