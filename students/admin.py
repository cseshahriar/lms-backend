# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Student, StudentCourseEnrolment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'password',
        'qualification',
        'mobile_no',
        'address',
        'interested_categories',
    )


@admin.register(StudentCourseEnrolment)
class StudentCourseEnrolmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'enrolled_time')
    list_filter = ('course', 'student', 'enrolled_time')
