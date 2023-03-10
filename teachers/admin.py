# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Teacher, CourseCategory, Course, Chapter


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'password',
        'qualification',
        'mobile_no',
        'skills',
    )


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'teacher', 'title', 'description')
    list_filter = ('category', 'teacher')


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'course',
        'title',
        'description',
        'video',
        'remarks',
    )
    list_filter = ('course',)
