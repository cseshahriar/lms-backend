# Generated by Django 4.1.7 on 2023-03-17 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_courserating'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(null=True, upload_to='student_images/'),
        ),
    ]
