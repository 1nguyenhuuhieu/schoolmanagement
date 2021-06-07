from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.db.models import F
from django.utils.text import slugify

LEVEL_CHOICES = [
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    ]
# Lấy khối học từ năm bắt đầu vào trường
def class_level_def(year):
    now = datetime.datetime.now()
    i = 0
    if (now.month < 9):
        i =  (now.year - year) + 5
    else:
        i = (now.year - year) + 6
    if i in [6,7,8,9]:
        return i
    else:
        return year

# năm học đang đào tạo
def schoolyear_learning():
    now = datetime.datetime.now()
    listyear = []
    for i in [1,2,3,4]:
        if now.month < 9:
            listyear.append(now.year - i)
        else:
            listyear.append(now.year + 1 -i )
    return listyear


#lấy niên khoá từ class level
def school_year_def(upload_time):
    if (upload_time.month < 9):
        return upload_time.year -1
    else:
        return upload_time.year

#lấy năm vào trường của lớp từ level
def level_to_startyear(level):
    now = datetime.datetime.now()
    if now.month < 9:
        return (now.year + 5 - level)
    else:
        return (now.year + 6 - level)

def q_schoolyear():
    now = datetime.datetime.now()
    current_startyear = school_year_def(now)
    schoolyear = Schoolyear.objects.get(start_date__year=current_startyear)
    return schoolyear
    

# có đang đào tạo tại trường
def is_learning_def(class_level):
    return class_level in [6,7,8,9]

# ABSTRACT MODEL ---------------------------------------------------------------

# Abstract for: School, Subject, GroupSubject
class SchoolAbstract(models.Model):
    title = models.CharField(max_length=50, verbose_name="Tiêu đề")
    description = models.CharField(max_length=200, verbose_name="Mô tả sơ lược", blank=True)
    cover = models.ImageField(upload_to="coverimages/", verbose_name="Ảnh bìa", null = True, blank = True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.title

# Abstract for: SubjectTeacher, ClassyearManager, GroupSubjectManager, SchoolManager
class MembershipAbstract(models.Model):
    teacher = models.ForeignKey(
        "Teacher",
        on_delete=models.CASCADE,
        verbose_name='Giáo viên',
        limit_choices_to={'is_work': True}
        )
    startdate = models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')
    enddate = models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')
    is_active = models.BooleanField(default=True, blank=True, verbose_name="Có hiệu lực không")
    schoolyear = models.ForeignKey(
        'Schoolyear',
        on_delete=models.CASCADE,
        default=q_schoolyear
    )

    class Meta:
        abstract = True

# MODEL ---------------------------------------------------------------------------
# GIÁO VIÊN
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Tài khoản đăng nhập")
    firstname = models.CharField("Họ",max_length=20, blank=True)
    lastname = models.CharField("Tên", max_length=20, blank=True)
    zalo_number = models.DecimalField(verbose_name="Số điện thoại",help_text="Số điện thoại có đăng ký zalo, sử dụng để nhận thông báo từ ban giám hiệu", max_digits=12, decimal_places=0,null=True, blank=True)
    birth_date = models.DateField("Ngày sinh", null=True, blank=True)
    SEX_CHOICES = [
    ('male', 'Nam'),
    ('female', 'Nữ')
    ]
    sex = models.CharField(verbose_name="Giới tính", max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    #chuyên môn chính
    main_subject = models.ForeignKey("Subject",on_delete=models.SET_NULL,null=True,blank=True, verbose_name="Chuyên môn chính")
    EDUCATION_LEVEL_CHOICES = [
        ('inter', 'Trung Cấp'),
        ('college', 'Cao Đẳng'),
        ('university', 'Đại Học'),
        ('master', 'Thạc Sĩ')
    ]
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, null=True, blank=True)
    is_work = models.BooleanField("Có đang công tác", default=True)
    def user_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    avatar = models.ImageField("Ảnh đại diện", upload_to=user_directory_path, blank=True, null=True)
    #tên đầy đủ
    def full_name(self):
        return ('%s %s') % (self.firstname, self.lastname)
    #tất cả giáo án
    def lesson_list(self):
        return self.lesson_set.filter(teacher = self.user.id)
    #môn dạy và lớp dạy phục vụ cho sidebar.html
    def current_schoolyear(self):
        now = datetime.datetime.now()
        current_startyear = school_year_def(now)
        schoolyear = Schoolyear.objects.get(start_date__year=current_startyear)
        return schoolyear
    
    def subject_classyear_list(self):
        return self.subjectclassyear_set.filter(
            schoolyear=self.current_schoolyear()).order_by('subject__subject__title').values('subject__subject__title', 'classyear__startyear__start_date__year','subject__subject__group__title').distinct()

    def subject_classyeartitle_list(self):
        return self.subjectclassyear_set.filter(
            schoolyear=self.current_schoolyear()).order_by('subject__subject__title').values('subject__subject__title', 'classyear__startyear__start_date__year','subject__subject__group__title', 'classyear__title','subject__total_lesson', 'subject__week_lesson').distinct()
    #giáo án mới nhất phục vụ trang dashboard
    def latest_lesson(self):
        return Lesson.objects.filter(teacher=self.user.teacher.id).order_by('-upload_time')[:3]
    #chức danh phục vụ cho trang dashboard
    def managers(self):
        managers = {}
        teacher = self.user.teacher.id
        group_manager = GroupSubjectManager.objects.filter(teacher=teacher).filter(is_active=True)
        if group_manager:
            group_manager = group_manager.latest('-id')
            managers['group'] = group_manager
        school_manager = SchoolManager.objects.filter(teacher=teacher).filter(is_active=True)
        if school_manager:
            school_manager = school_manager.latest('-id')
            managers['school'] = school_manager
        classyear_manager = ClassyearManager.objects.filter(teacher=teacher).filter(is_active=True)
        if classyear_manager:
            classyear_manager = classyear_manager.latest('-id')
            managers['class'] = classyear_manager
        return managers
    #thống kê số lượng giáo án
    def count_lesson(self):
        now = datetime.datetime.now()
        count = {}
        teacher = self.user.teacher.id
        lessons = Lesson.objects.filter(teacher=teacher)
        count['total'] = lessons.count()
        current_year = [school_year_def(now), school_year_def(now)+1]
        lesson_current_year = lessons.filter(upload_time__year__in = current_year )
        count['year'] = lesson_current_year.count()
        lesson_current_month =  lessons.filter(upload_time__year__in = current_year).filter(upload_time__month = now.month)
        count['month'] = lesson_current_month.count()
        return count

    def target_lesson_week(self):
        subjectclassyear = SubjectClassyear.objects.filter(
            schoolyear=self.current_schoolyear(), teacher=self.id
        )
        count = 0
        for i in subjectclassyear:
            count += i.subject.week_lesson

        return count

    def week_lesson(self):
        now = datetime.datetime.now()
        now_week = now.isocalendar()[1]
        teacher=self.id
        lesson_week = Lesson.objects.filter(
            teacher=teacher, upload_time__week=now_week
        )
        return(lesson_week.count())

    def is_complete_subjectclassyear(self):
        return self.week_lesson() >= self.target_lesson_week()

    class Meta:
        verbose_name = "Giáo viên"
        verbose_name_plural = "Giáo viên"

    def __str__(self):
        return self.full_name()

# TRƯỜNG HỌC
class School(SchoolAbstract):
    class Meta:
        verbose_name = "Trường Học"
        verbose_name_plural = "Trường Học"

# QUẢN LÝ TRƯỜNG HỌC
class SchoolManager(MembershipAbstract):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    ROLE_CHOICES = [
    ('submanager', 'Hiệu phó'),
    ('manager', 'Hiệu trưởng'),
    ('member', 'Khác')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='Vị trí')
    class Meta:
        verbose_name = "Quản lý trường học "
        verbose_name_plural = "Quản lý trường học"
    def __str__(self):
        return '%s - %s ' % (self.teacher.full_name(), self.role)
        
# NĂM HỌC        
class Schoolyear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Trường")
    total_week = models.IntegerField("Tổng số tuần học")
    start_date = models.DateField(help_text="Tuần 1 học kì 1 sẽ tính từ tuần này",  unique_for_year='start_date', verbose_name="Ngày học đầu tiên" )
    start_date_2 = models.DateField(help_text="Tuần 1 học kì 2 sẽ tính từ tuần này", blank=True, null=True, verbose_name="Ngày học đầu tiên học kì 2")
    end_date = models.DateField(blank=True, null=True, verbose_name="Ngày kết thúc năm học")
    spring_start = models.DateTimeField(help_text="Giờ mùa hè. Buổi sáng bắt đầu từ ngày nào, mấy giờ", blank=True, null=True, verbose_name="Giờ mùa hè") 
    winter_start = models.DateTimeField(help_text="Giờ mùa đông. Buổi sáng bắt đầu từ ngày nào, mấy giờ", blank=True, null=True,verbose_name="Giờ mùa đông") 
    
    # tuần của năm học
 
    class Meta:
        verbose_name = "Năm học"
        verbose_name_plural = "Năm học"
    def __str__(self):
        return '%s - %s' % (self.start_date.year, self.start_date.year + 1)

# LỚP HỌC
class Classyear(models.Model):
    TITLE_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
    ]
    title = models.CharField(verbose_name="Tên lớp", max_length=1, choices=TITLE_CHOICES)
    startyear = models.ForeignKey('Schoolyear', on_delete=models.CASCADE, verbose_name="Năm nhập học")
    @property
    def is_learning(self):
        return is_learning_def(class_level_def(self.startyear.start_date.year))
    @property
    def class_level(self):
        return class_level_def(self.startyear.start_date.year)
    def class_title_year(self):
        return "%s%s" % (self.class_level, self.title)
    class Meta:
        unique_together = ('title', 'startyear')
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
    def __str__(self):
        return  self.class_title_year()

# GIÁO VIÊN CHỦ NHIỆM
class ClassyearManager(MembershipAbstract):
    classyear = models.ForeignKey(Classyear, on_delete=models.CASCADE)
        
    class Meta:
        verbose_name = "Giáo viên chủ nhiệm"
        verbose_name_plural = "Giáo viên chủ nhiệm"

    def __str__(self):
        return self.classyear.__str__()

# BỘ MÔN
class GroupSubject(SchoolAbstract):
    class Meta:
        verbose_name = "Bộ môn"
        verbose_name_plural = "Bộ môn"

# QUẢN LÝ BỘ MÔN
class GroupSubjectManager(MembershipAbstract):
    group = models.ForeignKey(GroupSubject, on_delete=models.CASCADE)
    ROLE_CHOICES = [
    ('submanager', 'Phó bộ môn'),
    ('manager', 'Trưởng bộ môn'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    class Meta:
        verbose_name = "Quản lý Bộ Môn"
        verbose_name_plural = "Quản lý Bộ Môn"
    def __str__(self):
        return '%s %s ' % (self.teacher.full_name(),  self.group.title)

# MÔN HỌC
class Subject(SchoolAbstract):
    group = models.ForeignKey(GroupSubject,on_delete=models.CASCADE, verbose_name='Bộ môn')
    subject_slug = models.SlugField(max_length=50, null=True, blank=True)
    def teachers(self):
        return Teacher.objects.filter(
            subjectclassyear__subject__subject=self.id
        )
    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
    def save(self, *args, **kwargs):
        self.subject_slug = slugify(self.title)
        super().save(*args, **kwargs)

# NGƯỜI DUYỆT GIÁO ÁN MÔN HỌC
class SubjectManager(MembershipAbstract):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Người duyệt giáo án"
        verbose_name_plural = "Người duyệt giáo án"
    
    def __str__(self):
        return '%s %s' % (self.teacher.full_name(), self.subject.title)

# CHI TIẾT MÔN HỌC CỤ THỂ
class SubjectDetail(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Môn học")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Khối học")
    total_lesson = models.IntegerField(verbose_name="Tổng số tiết")
    week_lesson = models.IntegerField(verbose_name="Số tiết mỗi tuần")

    class Meta:
        verbose_name = "Chi tiết môn học"
        verbose_name_plural = "Chi tiết môn học"
    def __str__(self):
        return '%s %s' % (self.subject, self.level)


# PHÂN PHỐI CHƯƠNG TRÌNH
class SubjectLesson(models.Model):
    subject = models.ForeignKey(SubjectDetail, on_delete=models.CASCADE, verbose_name="Môn học")
    number_lesson = models.IntegerField()
    title = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Phân phối chương trình'
        verbose_name_plural = 'Phân phối chương trình'
    def __str__(self):
        return '%s - Tiết %s' % (self.subject, self.number_lesson)

# PHÂN CÔNG GIẢNG DẠY
class SubjectClassyear(MembershipAbstract):
    subject = models.ForeignKey(SubjectDetail, on_delete=models.CASCADE)
    classyear = models.ManyToManyField(
        Classyear,
        limit_choices_to={'startyear__start_date__year__in': schoolyear_learning()}
        )
    
    def classyear_list(self):
        return ', '.join(classyear.__str__() for classyear in self.classyear.all())

    class Meta:
        verbose_name = "Phân công giảng dạy"
        verbose_name_plural = "Phân công giảng dạy"
        unique_together = ('subject', 'teacher', 'schoolyear')

    def __str__(self):
        return '%s : %s - %s' % (self.subject, self.classyear_list(), self.teacher.full_name())


        
# GIÁO ÁN
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    lesson_path = models.FileField(blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)
    edit_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectDetail, on_delete=models.CASCADE)
    number_lesson = models.IntegerField(help_text="Bài giảng số mấy")
    schoolyear = models.ForeignKey(Schoolyear, on_delete=models.CASCADE)
    week = models.IntegerField("Tuần")
    classyear = models.ManyToManyField(Classyear, through="LessonSchedule")
    #Kiểm tra giáo án
    STATUS_CHOICES = [
    ('pending', 'Chờ duyệt'),
    ('acept', 'Đã duyệt'),
    ('deny', 'Bị từ chối'),
    ]
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES ,default='pending')
    checker = models.ForeignKey('Teacher', related_name="lesson_checker" ,on_delete=models.SET_NULL, null=True, blank=True)
    check_date = models.DateTimeField(auto_now=True)
    note_checker = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = "Giáo Án"
        verbose_name_plural = "Giáo Án"
        ordering = ["-upload_time"]
        unique_together = ['subject', 'number_lesson', 'teacher']

    #niên khoá hiện tại
    def school_year(self):
        return school_year_def(self.upload_time)
    #năm vào trường của lớp học của bài giảng
    def start_year_level(self):
        now = datetime.datetime.now()
        if now.month < 9:
            return school_year_def(self.upload_time) - self.subject.level + 6
        else:
            return school_year_def(self.upload_time) - self.subject.level + 7
    # giáo án này lên lịch cho những lớp
    def classyear_list(self):
        return LessonSchedule.objects.filter(lesson=self.id)

    def __str__(self):
        return '%s : Bài %s - %s - %s' % (self.subject, self.number_lesson,self.title, self.teacher)

# LỊCH BÁO GIẢNG
class LessonSchedule(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)
    classyear = models.ForeignKey(Classyear, on_delete = models.CASCADE)
    teach_date_schedule = models.DateField()
    week = models.IntegerField(blank=True, null=True)
    SESSION_CHOICES = [
        ('morning', 'Buổi sáng'),
        ('afternoon', 'Buổi chiều'),
    ]
    session = models.CharField(max_length=15, choices=SESSION_CHOICES)
    ORDER_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    order_schedule = models.IntegerField(choices=ORDER_CHOICES)
        
    def dayofweek(self):
        return self.teach_date_schedule.weekday()

    class Meta:
        unique_together = ('teach_date_schedule', 'session', 'order_schedule', 'lesson')
        verbose_name = 'Lịch báo giảng'
        verbose_name_plural = 'Lịch báo giảng'
    
    def __str__(self):
        return '%s %s' % (self.lesson, self.classyear)
