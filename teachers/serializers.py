from rest_framework import serializers
from rest_framework.response import Response
from .models import Teacher, CourseCategory, Course, Chapter


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id', 'full_name', 'detail', 'email', 'password', 'qualification',
            'mobile_no', 'skills', 'teacher_courses'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }
        depth = 1


class CourseCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ('id', 'title', 'description', )


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'title', 'description', 'teacher',
            'featured_img', 'technologies', 'course_chapters',
            'related_courses'
        )
        depth = 1
        # depth 1 is like to_representation and course_chapters is related name

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['teacher'] = TeacherSerializer(instance.teacher).data
        # response['category'] = CourseCategorySerializer(instance.category).data
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
        response['course'] = CourseSerializer(instance.course).data
        return response
