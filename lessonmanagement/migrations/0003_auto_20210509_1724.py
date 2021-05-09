# Generated by Django 3.2 on 2021-05-09 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0002_auto_20210509_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classyear',
            name='startyear',
            field=models.IntegerField(verbose_name='Năm nhập học'),
        ),
        migrations.AlterField(
            model_name='groupsubjectmanager',
            name='role',
            field=models.CharField(choices=[('submanager', 'Phó bộ môn'), ('manager', 'Trưởng bộ môn')], max_length=10),
        ),
    ]