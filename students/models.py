from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from teachers.models import Course


class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField()
    interested_categories = models.TextField()
    photo = models.ImageField(upload_to='student_images/', null=True)

    def __str__(self):
        return self.full_name


class StudentCourseEnrolment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrolled_courses"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrolled_students"
    )
    enrolled_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'student']

    def __str__(self):
        return f"{self.course.title} - {self.student.full_name}"


class CourseRating(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='ratings'
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='ratings'
    )
    rating = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=False)
    rating_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['course', 'student']
