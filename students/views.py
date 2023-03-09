from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .serializers import (
    StudentSerializer
)
from .models import Student


class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class StudentDetailUpdateDeleteAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class StudentLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or email == '':
            return Response(
                {'error': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError as e:
            return Response({'email': e.message}, status=400)

        if password is None or password == '':
            return Response(
                {'error': 'Password is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password and len(password) < 7:
            return Response(
                {'error': 'Password length minimum 7 characters.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        teacher = Student.objects.filter(email=email).first()
        if teacher:
            if check_password(password, teacher.password):
                data = {
                    'student_id': teacher.id,
                    'student_full_name': teacher.full_name,
                    'student_email': teacher.email
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {'error': 'User did not found.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
