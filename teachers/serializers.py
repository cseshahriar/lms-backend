from rest_framework import serializers
from .models import Teacher, CourseCategory, Course, Chapter


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
    class Meta:
        model = Course
        fields = (
            'id', 'category', 'title', 'description', 'teacher',
            'featured_img', 'technologies'
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['teacher'] = TeacherSerializer(instance.teacher).data
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
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['course'] = CourseSerializer(instance.teacher).data
        return response
