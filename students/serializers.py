from rest_framework import serializers
from rest_framework.response import Response
from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = (
            'id', 'full_name', 'email', 'password', 'qualification',
            'mobile_no', 'address', 'interested_categories'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }
        depth = 1
