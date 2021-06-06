# Generated by Django 3.2 on 2021-06-06 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0003_schoolyear_total_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='schoolyear',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.schoolyear'),
            preserve_default=False,
        ),
    ]
