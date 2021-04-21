# Generated by Django 3.2 on 2021-04-20 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0013_lesson_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='level',
            field=models.IntegerField(blank=True, choices=[('6', 6), ('7', 7), ('8', 8), ('9', 9)], null=True),
        ),
    ]