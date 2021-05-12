from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.db.models import F
from django.utils.text import slugify
from django.forms import ModelForm



#lấy class level từ năm bắt đầu vào trường
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

def is_learning_def(class_level):
    return class_level in [6,7,8,9]



#Abstract for: School, Subject, GroupSubject
class SchoolAbstract(models.Model):
    title = models.CharField(max_length=50, verbose_name="Tiêu đề")
    description = models.CharField(max_length=200, verbose_name="Mô tả sơ lược", blank=True)
    cover = models.ImageField(upload_to="coverimages/", verbose_name="Ảnh bìa", null = True, blank = True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

#Trường học
class School(SchoolAbstract):
    class Meta:
        verbose_name = "Trường Học"
        verbose_name_plural = "Trường Học"

#Môn học
class Subject(SchoolAbstract):
    group = models.ForeignKey("GroupSubject",on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Bộ môn')
    subject_slug = models.SlugField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
    
    def save(self, *args, **kwargs):
        self.subject_slug = slugify(self.title)
        super().save(*args, **kwargs)

class SubjectLesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
    LEVEL_CHOICES = [
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Khối')
    total_lesson = models.IntegerField(verbose_name='Tổng số tiết')
    week_lesson = models.IntegerField(verbose_name='Số tiết mỗi tuần')
    def __str__(self):
        return '%s - %s' %(self.subject, self.level)


#Bộ môn
class GroupSubject(SchoolAbstract):
    class Meta:
        verbose_name = "Bộ môn"
        verbose_name_plural = "Bộ môn"

#Abstract for: SubjectTeacher, ClassyearManager, GroupSubjectManager, SchoolManager
class MembershipAbstract(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, verbose_name='Giáo viên')
    startdate = models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')
    enddate = models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')
    is_active = models.BooleanField(default=True, blank=True, verbose_name="Có hiệu lực không", help_text="Không: Nếu giáo viên đã nghỉ hưu hoặc thôi việc")

    class Meta:
        abstract = True


#Giáo viên và môn học
class SubjectTeacher(MembershipAbstract):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ROLE_CHOICES = [
    ('member', 'Thành viên'),
    ('manager', 'Tổ trưởng'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    class Meta:
        
        verbose_name = "Thành Viên/Quản lý Môn học"
        verbose_name_plural = "Thành Viên/Quản lý Môn học"
    def __str__(self):
        return '%s %s' % (self.teacher.full_name(), self.subject.title)

#Giáo viên chủ nhiệm
class ClassyearManager(MembershipAbstract):
    classyear = models.ForeignKey("Classyear", on_delete=models.CASCADE)
        
    class Meta:
        verbose_name = "Giáo viên chủ nhiệm"
        verbose_name_plural = "Giáo viên chủ nhiệm"

    def __str__(self):
        return self.classyear.__str__()

#Giáo viên quản lý bộ môn
class GroupSubjectManager(MembershipAbstract):
    group = models.ForeignKey(GroupSubject, on_delete=models.CASCADE)
    ROLE_CHOICES = [
    ('submanager', 'Phó bộ môn'),
    ('manager', 'Trưởng bộ môn'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    class Meta:
        verbose_name = "Thành Viên/Quản lý Bộ Môn"
        verbose_name_plural = "Thành Viên/Quản lý Bộ Môn"
    def __str__(self):
        return '%s %s ' % (self.teacher.full_name(),  self.group.title)

# Ban giám hiệu nhà trường
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
        return '%s - %s ' % (self.teacher.full_name(),  self.role)

#Lớp học
class Classyear(models.Model):
    TITLE_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D')
    ]
    title = models.CharField(verbose_name="Tên lớp", max_length=1, choices=TITLE_CHOICES)
    startyear = models.IntegerField(verbose_name='Năm nhập học')

    @property
    def is_learning(self):
        return is_learning_def(class_level_def(self.startyear))

    @property
    def class_level(self):
        return class_level_def(self.startyear)

    
    def class_title_year(self):
        return "%s%s" % (self.class_level, self.title)

    class Meta:
        unique_together = ('title', 'startyear')
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"


    def __str__(self):
        return  self.class_title_year()

#Hồ sơ giáo viên
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Tài khoản đăng nhập", help_text="Tài khoản đăng nhập viết liền không dấu. Ví dụ: nhhieu. Viết tắt của Nguyễn Hữu Hiếu. Nếu trùng họ tên thì thêm số vào sau, ví dụ nhhieu2")
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
    

    is_work = models.BooleanField("Có đang công tác",default=True, help_text="Tích vào ô nếu đang công tác tại trường, bỏ tích nếu đã nghỉ hưu hoặc chuyển sang đơn vị khác")
    def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    # Bổ sung trình crop ảnh
    avatar = models.ImageField("Ảnh đại diện", help_text = "Ảnh nên được crop về ảnh vuông để đạt được độ thẩm mỹ cao nhất",upload_to = user_directory_path, blank = True, null = True)
    
    def full_name(self):
        return ('%s %s') % (self.firstname, self.lastname)
    
    class Meta:
        verbose_name = "Giáo viên"
        verbose_name_plural = "Giáo viên"

    def __str__(self):
        return self.full_name()

    #niên khóa hiện tại
    def schoolyear(self):
        now = datetime.datetime.now()
        if now.month < 9:
            return ('%s - %s') % (now.year - 1, now.year)
        else:
            return ('%s - %s') % (now.year, now.year+1)



    #tất cả giáo án
    def lesson_list(self):
        return self.lesson_set.filter(teacher = self.user.id)
    #môn dạy và lớp dạy phục vụ cho sidebar.html
    def subject_classyear_list(self):
        return self.subjectclassyear_set.filter(is_teach_now = True).order_by('subject__title').values('subject__title', 'classyear__startyear','subject__group__title').distinct()
    def subject_classyeartitle_list(self):
        return self.subjectclassyear_set.filter(is_teach_now = True).order_by('subject__title').values('subject__title', 'classyear__startyear','subject__group__title', 'classyear__title').distinct()

    #giáo án mới nhất phục vụ trang dashboard
    def latest_lesson(self):
        return Lesson.objects.filter(teacher=self.user.teacher.id).order_by('-upload_time')[:3]

    #chức danh phục vụ cho trang dashboard
    def managers(self):
        managers = {}
        teacher = self.user.teacher.id
        
        subject_manager = SubjectTeacher.objects.filter(teacher=teacher).filter(is_active = True)
        if subject_manager:
            subject_manager = subject_manager.latest('-id')
            managers['subject'] = subject_manager

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



    

#Giáo án
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    lesson_path = models.FileField(blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)
    edit_time = models.DateTimeField(blank=True, null=True)
    LEVEL_CHOICES = [
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)
    description = models.CharField(max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number_lesson = models.IntegerField(help_text="Bài giảng số mấy")
 
    schoolyear = models.ForeignKey("Schoolyear", on_delete=models.CASCADE, blank=True, null=True)

    classyear = models.ManyToManyField(Classyear, through="LessonClassyear")
    
    #Kiểm tra giáo án
    STATUS_CHOICES = [
    ('pending', 'Chờ duyệt'),
    ('acept', 'Đã duyệt'),
    ('deny', 'Bị từ chối'),
    ]
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES ,default='pending')
    checker = models.ForeignKey(Teacher, related_name="lesson_checker" ,on_delete=models.SET_NULL, null=True, blank=True)
    check_date = models.DateTimeField(auto_now=True)
    note_checker = models.CharField(max_length=200, blank=True)


    
    class Meta:
        verbose_name = "Giáo Án"
        verbose_name_plural = "Giáo Án"
        ordering = ["-upload_time"]
        unique_together = ['level', 'subject', 'number_lesson']


    #niên khoá hiện tại
    def school_year(self):
        return school_year_def(self.upload_time)

    #năm vào trường của lớp học của bài giảng
    def start_year_level(self):
        if now.month < 9:
            return school_year_def(self.upload_time) - self.level + 6
        else:
            return school_year_def(self.upload_time) - self.level + 7

    # giáo án này lên lịch cho những lớp
    def classyear_list(self):
        return LessonClassyear.objects.filter(lesson=self.id)
    def __str__(self):
        return '%s - %s' % (self.title, self.level)

# chương trình giảng dạy
class SubjectLevel(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    LEVEL_CHOICES = [
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES)
    number_lesson = models.IntegerField()
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return '%s - %s' % (self.subject, self.level)

#Giáo án thuộc lớp học nào
class LessonClassyear(models.Model):
    is_teach = models.BooleanField(default=False)
    teach_date = models.DateField(blank=True, null=True)
    
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)
    classyear = models.ForeignKey(Classyear, on_delete = models.CASCADE)
    
    teach_date_schedule = models.DateField(blank=True, null=True)
    week = models.IntegerField(blank=True, null=True)
    SESSION_CHOICES = [
        ('morning', 'Buổi sáng'),
        ('afternoon', 'Buổi chiều'),
    ]
    session = models.CharField(max_length=15, choices=SESSION_CHOICES, blank=True, null=True)
    ORDER_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    order_schedule = models.IntegerField(choices=ORDER_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('teach_date_schedule', 'session', 'order_schedule')
        verbose_name = 'Lịch báo giảng'
        verbose_name_plural = 'Lịch báo giảng'
        
    # def save(self, *args, **kwargs):
    #     self.week = self.teach_date_schedule.isocalendar()[1]
    #     super().save(*args, **kwargs)

    def dayofweek(self):
        return self.teach_date_schedule.day

    
    def __str__(self):
        return '%s %s %s' % (self.lesson, self.classyear, self.is_teach)

#Môn học cụ thể cho lớp cụ thể
class SubjectClassyear(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classyear = models.ManyToManyField(Classyear)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    schoolyear = models.ForeignKey("Schoolyear", on_delete=models.CASCADE)
    is_teach_now = models.BooleanField(default=True, verbose_name="Trạng thái hiệu lực")
    #update when current_lesson change
    edit_time = models.DateTimeField(auto_now=True, blank=True, null=True)
    def classyear_list(self):
        return ', '.join(classyear.__str__() for classyear in self.classyear.all())
    class Meta:
        verbose_name = "Phân công giảng dạy"
        verbose_name_plural = "Phân công giảng dạy"
        # ordering = ('subject__title', '-classyear__startyear')
        unique_together = ('subject', 'teacher')
    def __str__(self):
        return '%s : %s - %s' % (self.subject, self.classyear_list(), self.teacher.full_name())



class News(models.Model):
    creater = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="create_news")
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.FileField(upload_to="news/", verbose_name="File đính kèm trong tin tức", null = True, blank = True)
    upload_time = models.DateTimeField(auto_now=True)

    viewer = models.ManyToManyField(Teacher, blank=True, null=True)

    class Meta:
        ordering = ['upload_time']

    def __str__(self):
        return self.title


class Schoolyear(models.Model):
    start_date = models.DateField(help_text="Ngày bắt đầu năm học",  unique_for_year='start_date' )
    end_date = models.DateField(blank=True, null=True)

    spring_start = models.DateTimeField(help_text="Giờ mùa hè. Buổi sáng bắt đầu từ ngày nào, mấy giờ", blank=True, null=True) 

    winter_start = models.DateTimeField(help_text="Giờ mùa đông. Buổi sáng bắt đầu từ ngày nào, mấy giờ", blank=True, null=True) 

    class Meta:
        verbose_name = "Năm học"
        verbose_name_plural = "Năm học"
       

    def __str__(self):
        return '%s - %s' % (self.start_date.year, self.start_date.year + 1)
