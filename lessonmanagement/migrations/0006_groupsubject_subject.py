# Generated by Django 3.2 on 2021-04-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0005_alter_subject_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsubject',
            name='subject',
            field=models.ManyToManyField(to='lessonmanagement.Subject'),
        ),
    ]
