from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=20)
    skills = models.TextField()

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

    def __str__(self):
        return self.title


def video_upload_path(instance, filename):
    """Custom file 'upload_to' directory returned from formatted string"""
    return f'chapter/{instance.id}/videos/{filename}'


class Chapter(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT,
        related_name='course_chapters'
    )
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    video = models.FileField(upload_to=video_upload_path, null=True)
    remarks = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return self.title
