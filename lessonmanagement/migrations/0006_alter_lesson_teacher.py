# Generated by Django 3.2 on 2021-04-26 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0005_auto_20210426_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessonmanagement.teacher'),
        ),
    ]
