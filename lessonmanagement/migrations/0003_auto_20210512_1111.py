# Generated by Django 3.2 on 2021-05-12 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0002_remove_subjectclassyear_current_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='cout_number_lesson',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='start_number_lesson',
        ),
        migrations.AddField(
            model_name='lesson',
            name='number_lesson',
            field=models.IntegerField(default=1, help_text='Bài giảng số mấy'),
            preserve_default=False,
        ),
    ]
