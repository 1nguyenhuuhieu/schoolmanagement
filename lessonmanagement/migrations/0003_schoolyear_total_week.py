# Generated by Django 3.2 on 2021-06-06 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0002_auto_20210606_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolyear',
            name='total_week',
            field=models.IntegerField(default=40, verbose_name='Tổng số tuần học'),
            preserve_default=False,
        ),
    ]