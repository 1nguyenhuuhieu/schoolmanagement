# Generated by Django 3.2 on 2021-05-05 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0030_alter_schoolyear_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonclassyear',
            name='week',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]