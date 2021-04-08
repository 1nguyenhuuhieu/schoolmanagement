from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    firstname = models.CharField("họ",max_length=200)
    lastname = models.CharField("Tên", max_length=200)
    zalo_number = models.DecimalField(verbose_name="Số điện thoại",help_text="Số điện thoại có đăng ký zalo, sử dụng để nhận thông báo từ ban giám hiệu", max_digits=12, decimal_places=0)
    birth_date = models.DateField("Ngày sinh")
    SEX_CHOICES = [
    ('male', 'Nam'),
    ('female', 'Nữ')
    ]
    sex = models.CharField(verbose_name="Giới tính",max_length=6, choices=SEX_CHOICES)
    main_subject = models.ForeignKey("Subject", on_delete = models.SET_NULL, null=True, blank=True, verbose_name="Chuyên môn")
    is_work = models.BooleanField("Có đang công tác",default=True, help_text="Tích vào ô nếu đang công tác tại trường, bỏ tích nếu đã nghỉ hưu hoặc chuyển sang đơn vị khác")
    def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    # Bổ sung trình crop ảnh vào tempate
    avatar = models.ImageField("Ảnh đại diện", help_text = "Ảnh nên được crop về ảnh vuông để đạt được độ thẩm mỹ cao nhất",upload_to = user_directory_path, blank = True, null = True)

  

    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)


class SubjectAbstract(models.Model):
    title = models.CharField(max_length=20, verbose_name="Tên môn học", help_text="Tên chính xác của môn học theo quy định của Bộ Giáo Dục")
    description = models.TextField("Mô tả môn học", blank=True)
    coverimage = models.ImageField("Ảnh bìa cho môn học", upload_to = "subject/", null = True, blank = True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Subject(SubjectAbstract):
    group = models.ForeignKey("GroupSubject", on_delete=models.SET_NULL, null=True, blank=True)

class GroupSubject(SubjectAbstract):
    pass


class ManagerAbstract(models.Model):
    manager = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    note = models.CharField("Ghi chú", max_length=200,blank=True, null=True)


    class Meta:
        abstract = True



class SubjectManager(ManagerAbstract):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = [
    ('member', 'Thành viên'),
    ('leader', 'Lãnh đạo'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    def __str__(self):
        return '%s %s %s' % (self.manager.firstname, self.manager.lastname, self.subject.title)

class GroupSubjectManager(ManagerAbstract):
    group = models.ForeignKey(GroupSubject, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return '%s %s %s' % (self.manager.firstname, self.manager.lastname, self.group.title)


class ClassYear(models.Model):
    TITLE_CHOICES = [
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D')
    ]
    title = models.CharField(verbose_name="Tên lớp",max_length=1, choices=TITLE_CHOICES)
    startyear = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.title, self.startyear)

    def class_status(self):
        now = datetime.now()
        if (self.startyear + 3) > now.year:
            return "Đang đào tạo"
        else:
            return "Đã tốt nghiệp"

    def class_level(self):
        now = datetime.now()
        if (self.startyear) == now.year:
            return "6"
        elif (self.startyear + 1) == now.year:
            return "7"
        elif (self.startyear + 2) == now.year:
            return "8"
        elif (self.startyear + 3) == now.year:
            return "9"
        else:
            return "Đã tốt nghiệp"

class ClassYearManager(ManagerAbstract):
    class_year = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    upload_time = models.DateTimeField(auto_now=True)

 
    lesson_path = models.FileField(upload_to='test/')
    description = models.CharField(max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, related_name="teacher", on_delete=models.SET_NULL, null=True, blank=True)
    checker = models.ForeignKey(Teacher, related_name="checker", on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    start_number_lesson = models.IntegerField(null=True, blank=True)
    end_number_lesson = models.IntegerField(null=True, blank=True)

    class_year = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)
    STATUS_CHOICES = [
    ('pending', 'Chờ duyệt'),
    ('acept', 'Đã duyệt'),
    ('deny', 'Bị từ chối'),
    ]
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES)
    note_checker = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return self.title





