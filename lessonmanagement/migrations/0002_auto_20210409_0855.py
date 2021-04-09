# Generated by Django 3.1.7 on 2021-04-09 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teacher',
            options={},
        ),
        migrations.AddField(
            model_name='subject',
            name='member',
            field=models.ManyToManyField(through='lessonmanagement.SubjectManager', to='lessonmanagement.Teacher'),
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='class_year',
        ),
        migrations.AddField(
            model_name='lesson',
            name='class_year',
            field=models.ManyToManyField(blank=True, null=True, to='lessonmanagement.ClassYear'),
        ),
    ]