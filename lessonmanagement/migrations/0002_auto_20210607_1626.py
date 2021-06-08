# Generated by Django 3.2 on 2021-06-07 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classyearmanager',
            name='schoolyear',
            field=models.ForeignKey(limit_choices_to={'start_date__year': 2020}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
        migrations.AlterField(
            model_name='groupsubjectmanager',
            name='schoolyear',
            field=models.ForeignKey(limit_choices_to={'start_date__year': 2020}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
        migrations.AlterField(
            model_name='schoolmanager',
            name='schoolyear',
            field=models.ForeignKey(limit_choices_to={'start_date__year': 2020}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
        migrations.AlterField(
            model_name='subjectclassyear',
            name='schoolyear',
            field=models.ForeignKey(limit_choices_to={'start_date__year': 2020}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
        migrations.AlterField(
            model_name='subjectmanager',
            name='schoolyear',
            field=models.ForeignKey(limit_choices_to={'start_date__year': 2020}, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
        ),
    ]