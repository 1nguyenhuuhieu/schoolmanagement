# Generated by Django 3.1.7 on 2021-04-07 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0002_auto_20210407_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='avatar',
            field=models.ImageField(default=1, upload_to='imgs/avatar/'),
            preserve_default=False,
        ),
    ]
