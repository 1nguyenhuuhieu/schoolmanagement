# Generated by Django 3.2 on 2021-04-15 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classyear',
            options={'verbose_name': 'Lớp học', 'verbose_name_plural': 'Lớp học'},
        ),
        migrations.AddField(
            model_name='subjectclassyear',
            name='enddate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subjectclassyear',
            name='startdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
