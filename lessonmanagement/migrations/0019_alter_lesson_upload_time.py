# Generated by Django 3.2 on 2021-05-03 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0018_alter_news_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
