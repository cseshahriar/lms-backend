from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from .models import (
    Student, StudentCourseEnrolment, CourseRating, StudentFavoriteCourse,
    StudentAssignment
)
from teachers.serializers import CourseSerializer, TeacherSerializer


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'id', 'full_name', 'email', 'password', 'qualification',
            'mobile_no', 'address', 'interested_categories', 'photo'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }
        depth = 1


class StudentPasswordChangeSerializer(serializers.Serializer):
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

        user = Student.objects.filter(pk=pk).first()
        if user is None:
            raise serializers.ValidationError({
                "new_password": "User does not exist."
            })

        if not check_password(data['old_password'], user.password):
            raise serializers.ValidationError({
                "old_password": "Old Passwords do not match."
            })

        return data


class StudentCourseEnrolmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseEnrolment
        fields = ('id', 'course', 'student', 'enrolled_time', 'is_paid')

        validators = [
            UniqueTogetherValidator(
                queryset=StudentCourseEnrolment.objects.all(),
                fields=['course', 'student'],
                message="This course you are already taken."
            )
        ]

    def __init__(self, *args, **kwargs):
        super(StudentCourseEnrolmentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1


class StudentFavoriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFavoriteCourse
        fields = ('id', 'course', 'student', 'status')

        validators = [
            UniqueTogetherValidator(
                queryset=StudentFavoriteCourse.objects.all(),
                fields=['course', 'student'],
                message="This course you are already favorite."
            )
        ]

    def __init__(self, *args, **kwargs):
        super(StudentFavoriteCourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth = 0
        if request and request.method == 'GET':
            self.Meta.depth = 1


class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = (
            'id', 'course', 'student', 'rating', 'comment', 'rating_time',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=CourseRating.objects.all(),
                fields=['course', 'student'],
                message="Already review given for this course."
            )
        ]

    def validate(self, data):
        validation_fields = ['comment', ]
        errors = {}
        for validation_field in validation_fields:
            if validation_field not in data or data[validation_field] is None:
                errors[f"{validation_field}"] = "This field is required."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['course'] = CourseSerializer(instance.course).data
        response['student'] = StudentSerializer(instance.student).data
        return response


class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAssignment
        fields = (
            'id', 'teacher', 'student', 'title', 'detail', 'student_status',
            'created_at',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = StudentSerializer(instance.student).data
        response['teacher'] = TeacherSerializer(instance.teacher).data
        return response
