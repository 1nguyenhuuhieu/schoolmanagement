# Generated by Django 3.2 on 2021-04-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0011_alter_lesson_upload_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='upload_time',
            field=models.DateTimeField(),
        ),
    ]