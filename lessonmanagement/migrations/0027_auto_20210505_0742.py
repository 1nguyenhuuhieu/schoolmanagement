# Generated by Django 3.2 on 2021-05-05 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0026_rename_sprint_duration_schoolyear_spring_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schoolyear',
            name='spring_duration',
        ),
        migrations.RemoveField(
            model_name='schoolyear',
            name='spring_start',
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='spring_afternoon_end',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa hè. Buổi chiều kết thúc vào mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='spring_afternoon_start',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa hè. Buổi chiều bắt đầu từ ngày nào, mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='spring_morning_end',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa hè. Buổi sáng kết thúc vào mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='spring_morning_start',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa hè. Buổi sáng bắt đầu từ ngày nào, mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='winter_afternoon_end',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa đông. Buổi chiều kết thúc vào mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='winter_afternoon_start',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa đông. Buổi chiều bắt đầu từ ngày nào, mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='winter_morning_end',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa đông. Buổi sáng kết thúc vào mấy giờ', null=True),
        ),
        migrations.AddField(
            model_name='schoolyear',
            name='winter_morning_start',
            field=models.DateTimeField(blank=True, help_text='Giờ mùa đông. Buổi sáng bắt đầu từ ngày nào, mấy giờ', null=True),
        ),
    ]
