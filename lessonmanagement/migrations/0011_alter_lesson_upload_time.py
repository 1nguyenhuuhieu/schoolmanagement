# Generated by Django 3.2 on 2021-04-19 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0010_alter_lesson_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]