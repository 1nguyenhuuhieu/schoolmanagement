# Generated by Django 3.2 on 2021-04-21 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0020_auto_20210421_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupsubjectmanager',
            options={'verbose_name': 'Quản lý Bộ môn', 'verbose_name_plural': 'Quản lý Bộ môn'},
        ),
        migrations.AlterModelOptions(
            name='subjectteacher',
            options={'verbose_name': 'Thành Viên/Quản lý Môn học', 'verbose_name_plural': 'Thành Viên/Quản lý Môn học'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Giáo viên', 'verbose_name_plural': 'Giáo viên'},
        ),
    ]
