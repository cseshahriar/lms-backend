from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from teachers.models import Course, Teacher


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

    def total_enrolled_students(self):
        return self.enrolled_students.all().count()

    def total_favorite_students(self):
        return self.favorite_students.all().count()

    def total_complete_assignments(self):
        return self.assignments.filter(student_status=True).count()

    def total_pending_assignments(self):
        return self.assignments.filter(student_status=False).count()


class StudentCourseEnrolment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrolled_courses"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrolled_students"
    )
    enrolled_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

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


class StudentFavoriteCourse(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="favorite_courses"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="favorite_students"
    )
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ['course', 'student']

    def __str__(self):
        return f"{self.course.title} - {self.student.full_name}"


class StudentAssignment(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name='assignments',
        null=True
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='assignments'
    )
    title = models.CharField(max_length=255)
    detail = models.TextField(null=True)
    student_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
