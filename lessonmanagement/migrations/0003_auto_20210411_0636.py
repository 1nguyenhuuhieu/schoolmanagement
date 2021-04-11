# Generated by Django 3.1.7 on 2021-04-11 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0002_auto_20210409_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectClassYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_lesson', models.IntegerField()),
                ('classyear', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessonmanagement.classyear')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessonmanagement.subject')),
                ('teacher', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessonmanagement.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='classyear',
            field=models.ManyToManyField(through='lessonmanagement.SubjectClassYear', to='lessonmanagement.ClassYear'),
        ),
    ]
