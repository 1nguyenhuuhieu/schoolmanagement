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
    def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)
    avatar = models.ImageField("Ảnh đại diện", help_text = "Ảnh nên được crop về ảnh vuông để đạt được độ thẩm mỹ cao nhất",upload_to = "test/", blank = True, null = True)


    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)






