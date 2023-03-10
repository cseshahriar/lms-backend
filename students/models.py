from django.db import models
from teachers.models import Course


class Student(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    address = models.TextField()
    interested_categories = models.TextField()

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
