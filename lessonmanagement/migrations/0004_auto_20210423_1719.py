# Generated by Django 3.2 on 2021-04-23 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0003_alter_subject_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='classyear',
            name='class_level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='main_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessonmanagement.subject', verbose_name='Chuyên môn chính'),
        ),
    ]
