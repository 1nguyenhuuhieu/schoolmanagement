# Generated by Django 3.2 on 2021-04-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0032_auto_20210422_1713'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessonclassyear',
            options={'verbose_name': 'Giáo án thuộc lớp nào', 'verbose_name_plural': 'Giáo án thuộc lớp nào'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='subjectclassyear',
            name='is_teach_now',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Trạng thái hiệu lực'),
        ),
    ]
