# Generated by Django 4.1.7 on 2023-03-17 03:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0009_teacher_detail'),
        ('students', '0002_studentcourseenrolment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='teachers.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='students.student')),
            ],
            options={
                'unique_together': {('course', 'student')},
            },
        ),
    ]
