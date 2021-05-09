# Generated by Django 3.2 on 2021-05-09 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0008_auto_20210509_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjectclassyear',
            name='min_lesson',
        ),
        migrations.RemoveField(
            model_name='subjectclassyear',
            name='total_lesson',
        ),
        migrations.AddField(
            model_name='subjectclassyear',
            name='subjectlesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.subjectlesson'),
            preserve_default=False,
        ),
    ]
