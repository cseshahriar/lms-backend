# Generated by Django 4.1.7 on 2023-03-19 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='courserating',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
