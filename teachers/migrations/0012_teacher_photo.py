# Generated by Django 4.1.7 on 2023-03-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0011_chapter_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='photo',
            field=models.ImageField(null=True, upload_to='teacher_images/'),
        ),
    ]
