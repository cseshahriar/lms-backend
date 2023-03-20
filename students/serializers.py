from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Student, StudentCourseEnrolment, CourseRating
from teachers.serializers import CourseSerializer


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


class StudentCourseEnrolmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseEnrolment
        fields = ('id', 'course', 'student', 'enrolled_time')

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
