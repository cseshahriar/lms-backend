# Generated by Django 4.1.7 on 2023-03-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_studentfavoritecourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourseenrolment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
