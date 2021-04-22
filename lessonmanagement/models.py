from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from django.db.models import F
from django.utils.text import slugify

now = datetime.now()

class School(models.Model):
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Tài khoản đăng nhập", help_text="Tài khoản đăng nhập viết liền không dấu. Ví dụ: nhhieu. Viết tắt của Nguyễn Hữu Hiếu. Nếu trùng họ tên thì thêm số vào sau, ví dụ nhhieu2")
    firstname = models.CharField("Họ",max_length=200, blank=True)
    lastname = models.CharField("Tên", max_length=200, blank=True)
    zalo_number = models.DecimalField(verbose_name="Số điện thoại",help_text="Số điện thoại có đăng ký zalo, sử dụng để nhận thông báo từ ban giám hiệu", max_digits=12, decimal_places=0,null=True, blank=True)
    birth_date = models.DateField("Ngày sinh", null=True, blank=True, help_text="Định dạng: năm - tháng - ngày. Ví dụ: 1990-04-21")
    SEX_CHOICES = [
    ('male', 'Nam'),
    ('female', 'Nữ')
    ]
    sex = models.CharField(verbose_name="Giới tính", max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    #chuyên môn chính
    main_subject = models.ForeignKey("Subject",on_delete=models.SET_NULL,null=True,blank=True)

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

    def yearold(self):
        return now.year - self.birth_date.year
    def full_name(self):
        return '%s %s' % (self.firstname, self.lastname)

    def total_lesson(self):
        return Lesson.objects.filter(teacher=self.id).count()
    def total_lesson_year(self):
        return Lesson.objects.filter(teacher=self.id).filter(upload_time__year = now.year ).count()
    def total_lesson_month(self):
        return Lesson.objects.filter(teacher=self.id).filter(upload_time__year = now.year ).filter(upload_time__month = now.month).count()


    def subjectclassyear(self):
        i = SubjectClassYear.objects.filter(teacher=self.id).filter(is_teach_now = True).order_by('subject__title', 'classyear__startyear').distinct()
        return i
      

    def list_subject_classyear(self):
        listyear = []
        if now.month > 9:
            listyear = [now.year, now.year-1, now.year-2]
        else:
            listyear = [now.year - 1, now.year-2, now.year-3]
        m = SubjectClassYear.objects.filter(teacher = self.id).filter(classyear__startyear__in = listyear).values_list('subject__title', 'classyear__startyear').distinct()
        t = []
        
        for i in m:
            i = list(i)
            i.append(i[1])
            t.append(i)

        if now.month > 9:
            for i in t:
                if i[1] == now.year:
                    i[1] = 6
                elif i[1] == now.year - 1:
                    i[1] = 7
                elif i[1] == now.year - 2:
                    i[1] = 8
                else:
                    i[1] = 9
        else:
            for i in t:
                if i[1] == now.year-1:
                    i[1] = 6
                elif i[1] == now.year - 2:
                    i[1] = 7
                elif i[1] == now.year - 3:
                    i[1] = 8
                else:
                    i[1] = 9
        return t


     
    def list_lesson(self):
        return Lesson.objects.filter(teacher=self.id)

    
    def latest_lesson(self):
        return Lesson.objects.filter(teacher=self.id)[:3]
    def classyear_list(self):
        if now.month < 9:
            return  SubjectClassYear.objects.filter(teacher=self.id).filter(startdate__year = now.year - 1 )
        else:
            return SubjectClassYear.objects.filter(teacher=self.id).filter(startdate__year = now.year)

    def all_lessons(self):
        return Lesson.objects.filter(teacher=self.id)
    def list_subject_manager(self):
        return SubjectTeacher.objects.filter(teacher=self.id).filter(enddate=None).filter(role = "manager")
    def list_groupsubject_manager(self):
        return GroupSubjectManager.objects.filter(teacher=self.id).filter(enddate=None)
    def list_school_manager(self):
        return SchoolManager.objects.filter(teacher=self.id).filter(enddate=None)
    def time_now(self):
        return now
    


    class Meta:
        verbose_name = "Giáo viên"
        verbose_name_plural = "Giáo viên"
  



    def __str__(self):
        return self.full_name()




class SubjectAbstract(models.Model):
    title = models.CharField(max_length=20, verbose_name="Tên môn học", help_text="Tên chính xác của môn học theo quy định của Bộ Giáo Dục")
    description = models.TextField("Mô tả môn học", blank=True)
    coverimage = models.ImageField("Ảnh bìa cho môn học", upload_to = "subject/", null = True, blank = True)
    
    class Meta:
        abstract = True
    def get_slug(self):
        return slugify(title)

    def __str__(self):
        return self.title

class Subject(SubjectAbstract):
    group = models.ForeignKey("GroupSubject", related_name='subject123',on_delete=models.SET_NULL, null=True, blank=True)
    subject_slug = models.SlugField(max_length=200, null=True, blank=True)
    member = models.ManyToManyField(Teacher, through="SubjectTeacher")
    classyear = models.ManyToManyField("ClassYear", through="SubjectClassYear")
    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
    def save(self, *args, **kwargs):
        value = self.title
        self.subject_slug = slugify(value)
        super().save(*args, **kwargs)


class GroupSubject(SubjectAbstract):
    subject = models.ManyToManyField(Subject)
    class Meta:
        verbose_name = "Bộ môn"
        verbose_name_plural = "Bộ môn"


class ManagerAbstract(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    note = models.CharField("Ghi chú", max_length=200,blank=True, null=True)


    class Meta:
        abstract = True



class SubjectTeacher(ManagerAbstract):
    subject = models.ForeignKey(Subject, related_name="subjectteacher",on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = [
    ('member', 'Thành viên'),
    ('manager', 'Tổ trưởng'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    class Meta:
        verbose_name = "Thành Viên/Quản lý Môn học"
        verbose_name_plural = "Thành Viên/Quản lý Môn học"
    def __str__(self):
        return '%s %s %s' % (self.teacher.firstname, self.teacher.lastname, self.subject.title)

class GroupSubjectManager(ManagerAbstract):
    group = models.ForeignKey(GroupSubject, on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = [
    ('member', 'Phó bộ môn'),
    ('manager', 'Trưởng bộ môn'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    class Meta:
        verbose_name = "Quản lý Bộ môn"
        verbose_name_plural = "Quản lý Bộ môn"
    def __str__(self):
        return '%s %s ' % (self.teacher.full_name(),  self.group.title)

class SchoolManager(ManagerAbstract):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = [
    ('member', 'Hiệu phó'),
    ('manager', 'Hiệu trưởng'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    class Meta:
        verbose_name = "Quản lý trường "
        verbose_name_plural = "Quản lý trường"
    def __str__(self):
        return '%s - %s ' % (self.teacher.full_name(),  self.role)







class ClassYear(models.Model):
    TITLE_CHOICES = [
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D')
    ]
    title = models.CharField(verbose_name="Tên lớp", max_length=1, choices=TITLE_CHOICES)
    startyear = models.IntegerField()
    lesson_list = models.ManyToManyField("Lesson", through="LessonClassYear")

    @property
    def is_learning(self):
        now = datetime.now()
        if (self.startyear + 3) > now.year:
            return True
        else:
            return False
    
    
    def class_level(self):
        now = datetime.now()
        if now.month < 9:
            if (self.startyear) == now.year - 1:
                return 6
            elif (self.startyear) == now.year -2:
                return 7
            elif (self.startyear) == now.year -3:
                return 8
            elif (self.startyear) == now.year -4:
                return 9
            else:
                return "Khoá %s - %s" %( self.startyear, self.startyear+3)
        else:
            if (self.startyear) == now.year:
                return 6
            elif (self.startyear) == now.year - 1:
                return 7
            elif (self.startyear) == now.year - 2:
                return 8
            elif (self.startyear) == now.year - 3:
                return 9
            else:
                return "Khoá %s - %s" %( self.startyear, self.startyear+3)

    
    def class_title_year(self):
        return "%s%s" % (self.class_level(), self.get_title_display())

    def class_year_manager_display(self):
        class_year_manager = ClassYearManager.objects.filter(class_year_id = self.id)

        if class_year_manager:
            for i in class_year_manager:
                if i.enddate:
                    return "Chưa có Giáo viên chủ nhiệm"
                else:
                    return i.teacher
        else:
            return "Chưa có Giáo viên chủ nhiệm"
    def list_title(self):
        return ', '.join(lesson.title for lesson in self.lesson_list.all())
                    


    class Meta:
        unique_together = ('title', 'startyear')
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"

  

    def __str__(self):
        return  self.class_title_year()

class ClassYearManager(ManagerAbstract):
    class_year = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)
        
    class Meta:
        verbose_name = "Giáo viên chủ nhiệm"
        verbose_name_plural = "Giáo viên chủ nhiệm"

    def __str__(self):
        return self.class_year


class Lesson(models.Model):
    title = models.CharField(max_length=200)
  
    upload_time = models.DateTimeField(auto_now_add=True)
    lesson_path = models.FileField(upload_to='test/')
    LEVEL_CHOICES = [
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9)
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, related_name="teacher", on_delete=models.SET_NULL, null=True, blank=True)
    checker = models.ForeignKey(Teacher, related_name="checker", on_delete=models.SET_NULL, null=True, blank=True)
    classyear_list = models.ManyToManyField(ClassYear, through="LessonClassYear")


    check_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    slug_subject = models.SlugField(max_length=200, null=True, blank=True)

    start_number_lesson = models.IntegerField(null=True, blank=True, help_text="Bài giảng này ở tiết số mấy")
    cout_number_lesson = models.IntegerField(null=True, blank=True, help_text="Bài giảng này trong bao nhiêu tiết")

    # class_year = models.ManyToManyField(ClassYear, null=True, blank=True ,through="LessonClassYear")
    STATUS_CHOICES = [
    ('pending', 'Chờ duyệt'),
    ('acept', 'Đã duyệt'),
    ('deny', 'Bị từ chối'),
    ]
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES ,default='pending')
    note_checker = models.CharField(max_length=200, blank=True)
    class Meta:
        verbose_name = "Giáo Án"
        verbose_name_plural = "Giáo Án"
        ordering = ["-upload_time"]

 

    def display_classyear(self):
        classyear_list1 = []
        for i in self.classyear_list.all():
            classyear_list1.append(i)
        return classyear_list1

    def save(self, *args, **kwargs):
        value = self.subject.title
        self.slug_subject = slugify(value)
        super().save(*args, **kwargs)



    def __str__(self):
        return '%s - %s' % (self.title, self.level)

class LessonClassYear(models.Model):
    is_teach = models.BooleanField(blank=True, null=True)
    teach_date = models.DateField(auto_now=True,blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    classyear = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        unique_together = ('lesson', 'classyear')
        verbose_name = 'Giáo án thuộc lớp nào'
        verbose_name_plural = 'Giáo án thuộc lớp nào'
    

    def __str__(self):
        return '%s %s %s' % (self.lesson, self.classyear, self.is_teach)




class SubjectClassYear(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    classyear = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)
    total_lesson = models.IntegerField(blank=True,null=True)
    current_lesson = models.IntegerField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,related_name='subjectclassyearlist')
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    is_teach_now = models.BooleanField(default=True,blank=True, null=True, verbose_name="Trạng thái hiệu lực")

    class Meta:
        verbose_name = "Phân công giảng dạy"
        verbose_name_plural = "Phân công giảng dạy"




    def __str__(self):
        return '%s %s - %s' % (self.subject, self.classyear, self.teacher.full_name())



