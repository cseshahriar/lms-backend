from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Student, StudentCourseEnrolment



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
        depth = 1
