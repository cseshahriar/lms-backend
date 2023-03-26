# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Student, StudentCourseEnrolment, CourseRating, StudentFavoriteCourse,
    StudentAssignment
)


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


@admin.register(StudentFavoriteCourse)
class StudentFavoriteCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'status')
    list_filter = ('course', 'student', )


@admin.register(CourseRating)
class CourseRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'rating', 'rating_time')
    list_filter = ('course', 'student',)

    ordering = ('-rating_time', )


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'title', 'detail')
    list_filter = ('student', 'title')

    ordering = ('-created_at', )
