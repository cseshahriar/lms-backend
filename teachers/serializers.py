from rest_framework import serializers
from rest_framework.response import Response
from django.core.validators import EmailValidator
from .models import Teacher, CourseCategory, Course, Chapter


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
            'id', 'full_name', 'detail', 'email', 'password', 'qualification',
            'mobile_no', 'skills', 'teacher_courses', 'skill_list'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
        }
        depth = 1


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
            'id', 'category', 'title', 'description', 'teacher',
            'featured_img', 'technologies',
            'skill_list', 'course_chapters', 'related_courses',
            'total_enrolled_students'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'category': {'required': True},
        }
        # depth = 1
        # depth 1 is like to_representation and course_chapters is related name

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
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['course'] = CourseSerializer(instance.course).data
        return response
