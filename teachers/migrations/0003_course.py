# Generated by Django 4.1.7 on 2023-02-20 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_coursecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category_courses', to='teachers.coursecategory')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teacher_courses', to='teachers.teacher')),
            ],
        ),
    ]