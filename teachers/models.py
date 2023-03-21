from django.core import serializers
from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    detail = models.TextField(null=True)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    skills = models.TextField()
    photo = models.ImageField(upload_to='teacher_images/', null=True)

    def total_courses(self):
        return self.teacher_courses.all().count()

    def total_chapters(self):
        return Chapter.objects.filter(course__teacher=self).count()

    def total_students(self):
        total = 0
        courses = self.teacher_courses.all()
        for course in courses:
            total += course.enrolled_courses.all().count()
        return total

    def skill_list(self):
        """ return list of skills"""
        return self.skills.split(',')

    def __str__(self):
        return self.full_name


class CourseCategory(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Course Categories"

    def __str__(self):
        return self.title


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
    featured_img = models.ImageField(upload_to='course_images/', null=True)
    technologies = models.TextField(null=True)
    duration = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def skill_list(self):
        """ return list of skills"""
        return self.technologies.split(',')

    def total_enrolled_students(self):
        return self.enrolled_courses.all().count()

    def course_rating(self):
        course_rating = self.ratings.all().aggregate(
            avg_rating=models.Avg('rating')
        )
        return course_rating['avg_rating']


def video_upload_path(instance, filename):
    """Custom file 'upload_to' directory returned from formatted string"""
    return f'chapter/{instance.pk}/videos/{filename}'


class Chapter(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT,
        related_name='course_chapters'
    )
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    video = models.FileField(upload_to=video_upload_path, null=True)
    remarks = models.TextField(null=True)
    duration = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return self.title
