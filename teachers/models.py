from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField()


class CourseCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()


class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory, on_delete=models.PROTECT,
        related_name='category_courses'
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.PROTECT, related_name='teacher_courses'
    )
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
