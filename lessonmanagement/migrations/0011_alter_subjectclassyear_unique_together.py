# Generated by Django 3.2 on 2021-05-09 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0010_remove_subjectclassyear_subjectlesson'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subjectclassyear',
            unique_together={('subject', 'teacher')},
        ),
    ]