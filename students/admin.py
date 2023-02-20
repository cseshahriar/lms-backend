# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Student


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
