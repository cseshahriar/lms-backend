from rest_framework import serializers
from .models import Teacher, CourseCategory, Course


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id', 'full_name', 'email', 'password', 'qualification',
            'mobile_no', 'skills',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ('id', 'title', 'description', )


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True, many=False)

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'title', 'description', 'teacher',
            'featured_img', 'technologies'
        )
