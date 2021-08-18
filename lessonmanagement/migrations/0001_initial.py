# Generated by Django 3.2.5 on 2021-08-17 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lessonmanagement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classyear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, verbose_name='Tên lớp')),
            ],
            options={
                'verbose_name': 'Lớp học',
                'verbose_name_plural': 'Lớp học',
            },
        ),
        migrations.CreateModel(
            name='GroupSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tiêu đề')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Mô tả sơ lược')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='coverimages/', verbose_name='Ảnh bìa')),
            ],
            options={
                'verbose_name': 'Bộ môn',
                'verbose_name_plural': 'Bộ môn',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('lesson_path', models.FileField(blank=True, null=True, upload_to='')),
                ('upload_time', models.DateTimeField(blank=True, null=True)),
                ('edit_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('number_lesson', models.IntegerField(help_text='Bài giảng số mấy')),
                ('week', models.IntegerField(verbose_name='Tuần')),
                ('status', models.CharField(blank=True, choices=[('pending', 'Chờ duyệt'), ('acept', 'Đã duyệt'), ('deny', 'Bị từ chối')], default='pending', max_length=10)),
                ('check_date', models.DateTimeField(auto_now=True)),
                ('note_checker', models.CharField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Giáo Án',
                'verbose_name_plural': 'Giáo Án',
                'ordering': ['-upload_time'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tiêu đề')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Mô tả sơ lược')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='coverimages/', verbose_name='Ảnh bìa')),
            ],
            options={
                'verbose_name': 'Trường Học',
                'verbose_name_plural': 'Trường Học',
            },
        ),
        migrations.CreateModel(
            name='Schoolyear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_week', models.IntegerField(verbose_name='Tổng số tuần học')),
                ('start_date', models.DateField(help_text='Tuần 1 học kì 1 sẽ tính từ tuần này', unique_for_year='start_date', verbose_name='Ngày học đầu tiên')),
                ('start_date_2', models.DateField(blank=True, help_text='Tuần 1 học kì 2 sẽ tính từ tuần này', null=True, verbose_name='Ngày học đầu tiên học kì 2')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc năm học')),
                ('spring_start', models.DateTimeField(blank=True, help_text='Giờ mùa hè. Buổi sáng bắt đầu từ ngày nào, mấy giờ', null=True, verbose_name='Giờ mùa hè')),
                ('winter_start', models.DateTimeField(blank=True, help_text='Giờ mùa đông. Buổi sáng bắt đầu từ ngày nào, mấy giờ', null=True, verbose_name='Giờ mùa đông')),
                ('is_active', models.BooleanField(verbose_name='Năm học hiện tại')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.school', verbose_name='Trường')),
            ],
            options={
                'verbose_name': 'Năm học',
                'verbose_name_plural': 'Năm học',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Tiêu đề')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Mô tả sơ lược')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='coverimages/', verbose_name='Ảnh bìa')),
                ('subject_slug', models.SlugField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.groupsubject', verbose_name='Bộ môn')),
            ],
            options={
                'verbose_name': 'Môn học',
                'verbose_name_plural': 'Môn học',
            },
        ),
        migrations.CreateModel(
            name='SubjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('level', models.IntegerField(choices=[(6, 6), (7, 7), (8, 8), (9, 9)], verbose_name='Khối học')),
                ('total_lesson', models.IntegerField(verbose_name='Tổng số tiết')),
                ('week_lesson', models.IntegerField(verbose_name='Số tiết mỗi tuần')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subject', verbose_name='Môn học')),
            ],
            options={
                'verbose_name': 'Chi tiết môn học',
                'verbose_name_plural': 'Chi tiết môn học',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=20, verbose_name='Họ')),
                ('lastname', models.CharField(blank=True, max_length=20, verbose_name='Tên')),
                ('zalo_number', models.DecimalField(blank=True, decimal_places=0, help_text='Số điện thoại có đăng ký zalo, sử dụng để nhận thông báo từ ban giám hiệu', max_digits=12, null=True, verbose_name='Số điện thoại')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Ngày sinh')),
                ('sex', models.CharField(blank=True, choices=[('male', 'Nam'), ('female', 'Nữ')], max_length=6, null=True, verbose_name='Giới tính')),
                ('education_level', models.CharField(blank=True, choices=[('inter', 'Trung Cấp'), ('college', 'Cao Đẳng'), ('university', 'Đại Học'), ('master', 'Thạc Sĩ')], max_length=20, null=True)),
                ('is_work', models.BooleanField(default=True, verbose_name='Có đang công tác')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=lessonmanagement.models.Teacher.user_directory_path, verbose_name='Ảnh đại diện')),
                ('main_subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessonmanagement.subject', verbose_name='Chuyên môn chính')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Tài khoản đăng nhập')),
            ],
            options={
                'verbose_name': 'Giáo viên',
                'verbose_name_plural': 'Giáo viên',
            },
        ),
        migrations.CreateModel(
            name='SubjectLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_lesson', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subjectdetail', verbose_name='Môn học')),
            ],
            options={
                'verbose_name': 'Phân phối chương trình',
                'verbose_name_plural': 'Phân phối chương trình',
            },
        ),
        migrations.CreateModel(
            name='SchoolManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')),
                ('enddate', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Có hiệu lực không')),
                ('role', models.CharField(choices=[('submanager', 'Hiệu phó'), ('manager', 'Hiệu trưởng'), ('member', 'Khác')], max_length=10, verbose_name='Vị trí')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.school')),
                ('schoolyear', models.ForeignKey(default=lessonmanagement.models.q_schoolyear, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_work': True}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher', verbose_name='Giáo viên')),
            ],
            options={
                'verbose_name': 'Quản lý trường học ',
                'verbose_name_plural': 'Quản lý trường học',
            },
        ),
        migrations.CreateModel(
            name='LessonSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teach_date_schedule', models.DateField()),
                ('week', models.IntegerField(blank=True, null=True)),
                ('session', models.CharField(choices=[('morning', 'Buổi sáng'), ('afternoon', 'Buổi chiều')], max_length=15)),
                ('order_schedule', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('classyear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.classyear')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.lesson')),
            ],
            options={
                'verbose_name': 'Lịch báo giảng',
                'verbose_name_plural': 'Lịch báo giảng',
                'unique_together': {('teach_date_schedule', 'session', 'order_schedule', 'lesson')},
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='checker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson_checker', to='lessonmanagement.teacher'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='classyear',
            field=models.ManyToManyField(through='lessonmanagement.LessonSchedule', to='lessonmanagement.Classyear'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='schoolyear',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subjectdetail'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher'),
        ),
        migrations.CreateModel(
            name='GroupSubjectManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')),
                ('enddate', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Có hiệu lực không')),
                ('role', models.CharField(choices=[('submanager', 'Phó bộ môn'), ('manager', 'Trưởng bộ môn')], max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.groupsubject')),
                ('schoolyear', models.ForeignKey(default=lessonmanagement.models.q_schoolyear, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_work': True}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher', verbose_name='Giáo viên')),
            ],
            options={
                'verbose_name': 'Quản lý Bộ Môn',
                'verbose_name_plural': 'Quản lý Bộ Môn',
            },
        ),
        migrations.CreateModel(
            name='ClassyearManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')),
                ('enddate', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Có hiệu lực không')),
                ('classyear', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.classyear')),
                ('schoolyear', models.ForeignKey(default=lessonmanagement.models.q_schoolyear, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_work': True}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher', verbose_name='Giáo viên')),
            ],
            options={
                'verbose_name': 'Giáo viên chủ nhiệm',
                'verbose_name_plural': 'Giáo viên chủ nhiệm',
            },
        ),
        migrations.AddField(
            model_name='classyear',
            name='startyear',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear', verbose_name='Năm nhập học'),
        ),
        migrations.CreateModel(
            name='SubjectManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')),
                ('enddate', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Có hiệu lực không')),
                ('schoolyear', models.ForeignKey(default=lessonmanagement.models.q_schoolyear, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subject')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_work': True}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher', verbose_name='Giáo viên')),
            ],
            options={
                'verbose_name': 'Người duyệt giáo án',
                'verbose_name_plural': 'Người duyệt giáo án',
                'unique_together': {('teacher', 'subject', 'schoolyear')},
            },
        ),
        migrations.CreateModel(
            name='SubjectClassyear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(blank=True, null=True, verbose_name='Ngày bắt đầu')),
                ('enddate', models.DateField(blank=True, null=True, verbose_name='Ngày kết thúc')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Có hiệu lực không')),
                ('classyear', models.ManyToManyField(limit_choices_to={'startyear__start_date__year__in': [2020, 2019, 2018, 2017]}, to='lessonmanagement.Classyear')),
                ('schoolyear', models.ForeignKey(default=lessonmanagement.models.q_schoolyear, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subjectdetail')),
                ('teacher', models.ForeignKey(limit_choices_to={'is_work': True}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher', verbose_name='Giáo viên')),
            ],
            options={
                'verbose_name': 'Phân công giảng dạy',
                'verbose_name_plural': 'Phân công giảng dạy',
                'unique_together': {('subject', 'teacher', 'schoolyear')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('subject', 'number_lesson', 'teacher', 'schoolyear')},
        ),
        migrations.AlterUniqueTogether(
            name='classyear',
            unique_together={('title', 'startyear')},
        ),
    ]
