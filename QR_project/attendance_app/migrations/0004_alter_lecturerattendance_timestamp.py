# Generated by Django 5.0.4 on 2024-05-01 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0003_rename_time_fame_lecture_time_frame'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturerattendance',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
