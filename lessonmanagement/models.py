from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from django.db.models import F
# Create your models here.
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


    is_work = models.BooleanField("Có đang công tác",default=True, help_text="Tích vào ô nếu đang công tác tại trường, bỏ tích nếu đã nghỉ hưu hoặc chuyển sang đơn vị khác")
    def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    # Bổ sung trình crop ảnh vào tempate
    avatar = models.ImageField("Ảnh đại diện", help_text = "Ảnh nên được crop về ảnh vuông để đạt được độ thẩm mỹ cao nhất",upload_to = user_directory_path, blank = True, null = True)

    def full_name(self):
        return '%s %s' % (self.firstname, self.lastname)
    
    def list_classyear(self):
        return SubjectClassYear.objects.filter(teacher=self.user.id)



    def __str__(self):
        return '%s %s %s' % (self.firstname, self.lastname, self.main_subject)




class SubjectAbstract(models.Model):
    title = models.CharField(max_length=20, verbose_name="Tên môn học", help_text="Tên chính xác của môn học theo quy định của Bộ Giáo Dục")
    description = models.TextField("Mô tả môn học", blank=True)
    coverimage = models.ImageField("Ảnh bìa cho môn học", upload_to = "subject/", null = True, blank = True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Subject(SubjectAbstract):
    group = models.ForeignKey("GroupSubject", related_name='subject123',on_delete=models.SET_NULL, null=True, blank=True)
    member = models.ManyToManyField(Teacher, through="SubjectTeacher")
    classyear = models.ManyToManyField("ClassYear", through="SubjectClassYear")
    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"

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
    ('manager', 'Quản lý'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    def __str__(self):
        return '%s %s %s' % (self.teacher.firstname, self.teacher.lastname, self.subject.title)

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
    title = models.CharField(verbose_name="Tên lớp", max_length=1, choices=TITLE_CHOICES)
    startyear = models.IntegerField()

    @property
    def is_learning(self):
        now = datetime.now()
        if (self.startyear + 3) > now.year:
            return True
        else:
            return False
    
    


    def class_level(self):
        now = datetime.now()
        if (self.startyear) == now.year:
            return 6
        elif (self.startyear + 1) == now.year:
            return 7
        elif (self.startyear + 2) == now.year:
            return 8
        elif (self.startyear + 3) == now.year:
            return 9
        else:
            return "Đã tốt nghiệp khoá %s - %s" %( self.startyear, self.startyear+3)
    
    def class_title_year(self):
        return "%s %s" % (self.class_level(), self.get_title_display())

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
                    


    class Meta:
        unique_together = ('title', 'startyear')
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"

  

    def __str__(self):
        return  '%s %s' % (self.class_title_year(),self.class_year_manager_display())

class ClassYearManager(ManagerAbstract):
    class_year = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, null=True, blank=True)
        
    class Meta:
        verbose_name = "Giáo viên chủ nhiệm"
        verbose_name_plural = "Giáo viên chủ nhiệm"

    def __str__(self):
        return '%s - %s' % (self.class_year, self.teacher)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    upload_time = models.DateTimeField(auto_now_add=True)
    lesson_path = models.FileField(upload_to='test/')
    description = models.CharField(max_length=200, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, related_name="teacher", on_delete=models.SET_NULL, null=True, blank=True)
    checker = models.ForeignKey(Teacher, related_name="checker", on_delete=models.SET_NULL, null=True, blank=True)
    classyear = models.ManyToManyField(ClassYear, through="LessonClassYear")


    check_date = models.DateTimeField(auto_now = True, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)

    start_number_lesson = models.IntegerField(null=True, blank=True)
    end_number_lesson = models.IntegerField(null=True, blank=True)

    # class_year = models.ManyToManyField(ClassYear, null=True, blank=True ,through="LessonClassYear")
    STATUS_CHOICES = [
    ('pending', 'Chờ duyệt'),
    ('acept', 'Đã duyệt'),
    ('deny', 'Bị từ chối'),
    ]
    status = models.CharField(max_length=10, blank=True, choices=STATUS_CHOICES)
    note_checker = models.CharField(max_length=200, blank=True)
    class Meta:
        verbose_name = "Giáo Án"
        verbose_name_plural = "Giáo Án"

 

    def display_classyear(self):
        classyear_list = []
        for i in self.classyear.all():
            classyear_list.append(i)
        return classyear_list



    def __str__(self):
        return self.title

class LessonClassYear(models.Model):
    is_teach = models.BooleanField(blank=True, null=True)
    teach_date = models.DateField(blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    classyear = models.ForeignKey(ClassYear, on_delete=models.SET_NULL, blank=True, null=True)

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



    def __str__(self):
        return '%s %s %s %s' % (self.subject, self.classyear, self.teacher.firstname, self.teacher.lastname)

    





