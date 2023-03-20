import re
from rest_framework import serializers
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import authenticate
from .models import Teacher, CourseCategory, Course, Chapter


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id', 'full_name', 'detail', 'email', 'password', 'qualification',
            'mobile_no', 'skills', 'teacher_courses', 'skill_list', 'photo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
        }
        depth = 1


class TeacherDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id', 'full_name', 'detail', 'email', 'password', 'qualification',
            'mobile_no', 'skills', 'teacher_courses', 'skill_list', 'photo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required': False},
            'email': {'read_only': True, 'required': False},
            'photo': {'required': False},
        }
        depth = 1


class TeacherPasswordChangeSerializer(serializers.Serializer):
    pk = serializers.CharField(required=False)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        pk = int(data['pk'])
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "new_password": "Passwords does not match.",
            })

        user = Teacher.objects.filter(pk=pk).first()
        if user is None:
            raise serializers.ValidationError({
                "new_password": "User does not exist."
            })

        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({
                "old_password": "Old Passwords do not match."
            })

        return data


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ('id', 'title', 'description', )


class CourseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            'id',
            'title',
            'description',
            'video',
            'remarks',
            'duration'
        )


class RelatedCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'title', 'description', 'teacher',
            'featured_img', 'technologies',
        )


class CourseSerializer(serializers.ModelSerializer):
    course_chapters = CourseChapterSerializer(many=True, read_only=True)
    related_courses = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'title', 'description', 'duration', 'teacher',
            'featured_img', 'technologies',
            'skill_list', 'course_chapters', 'related_courses',
            'total_enrolled_students', 'course_rating'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'category': {'required': True},
        }

    def get_related_courses(self, obj):
        related_courses = Course.objects.filter(
            technologies__icontains=obj.technologies
        ).exclude(pk=obj.pk)
        related_course_serializer = RelatedCourseSerializer(related_courses, many=True)  # noqa
        return related_course_serializer.data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['teacher'] = TeacherSerializer(instance.teacher).data
        response['category'] = CourseCategorySerializer(instance.category).data
        return response


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = (
            'id',
            'course',
            'title',
            'description',
            'video',
            'remarks',
            'duration'
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['course'] = CourseSerializer(instance.course).data
        return response
