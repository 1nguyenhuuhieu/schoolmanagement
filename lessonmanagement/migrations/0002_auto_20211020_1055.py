# Generated by Django 3.2.8 on 2021-10-20 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupsubjectmanager',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupsubjectmanager',
            name='schoolyear',
        ),
        migrations.RemoveField(
            model_name='groupsubjectmanager',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='group',
        ),
        migrations.DeleteModel(
            name='GroupSubject',
        ),
        migrations.DeleteModel(
            name='GroupSubjectManager',
        ),
    ]
