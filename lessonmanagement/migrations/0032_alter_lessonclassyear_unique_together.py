# Generated by Django 3.2 on 2021-05-05 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessonmanagement', '0031_lessonclassyear_week'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lessonclassyear',
            unique_together={('teach_date_schedule', 'session', 'order_schedule')},
        ),
    ]
