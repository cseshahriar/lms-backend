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
    TeacherSerializer, TeacherDetailSerializer,
    TeacherPasswordChangeSerializer,
    CourseCategorySerializer, CourseSerializer,
    ChapterSerializer
)
from . import models


class TeacherListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class TeacherDetailUpdateDeleteAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherDetailSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def perform_update(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class TeacherLoginAPIView(APIView):
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

        teacher = models.Teacher.objects.filter(email=email).first()

        if teacher:
            if check_password(password, teacher.password):
                data = {
                    'teacher_id': teacher.id,
                    'teacher_full_name': teacher.full_name,
                    'teacher_email': teacher.email
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
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordChangeView(APIView):
    """ password change api view"""
    def post(self, request, format=None):
        serializer = TeacherPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            new_password = serializer.validated_data.get('new_password')
            user = models.Teacher.objects.filter(pk=pk).first()
            password = make_password(new_password)
            user.password = password
            user.save()
            return Response({'message': 'Password changed successfully.'})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CategoryListAPIView(generics.ListAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    # permission_classes = (permissions.IsAuthenticated, )


class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = super().get_queryset()

        if 'teacher_id' in self.request.GET:
            teacher_id = int(self.request.GET.get('teacher_id'))
            qs = qs.filter(
                teacher_id=teacher_id
            ).order_by('-id')

        if 'category' in self.request.GET:
            slug = self.request.GET.get('category')
            qs = qs.filter(
                category__title=slug
            ).order_by('-id')

        if 'limit' in self.request.GET:
            limit = int(self.request.GET.get('limit'))
            qs = qs.order_by('-id')[:limit]

        return qs


class CourseRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = (permissions.IsAuthenticated, )


class TeacherCourseListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = models.Teacher.objects.filter(id=teacher_id).first()
        return models.Course.objects.filter(teacher=teacher)


class ChapterListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course = models.Course.objects.filter(id=course_id).first()
        return models.Chapter.objects.filter(course=course)


class ChapterRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):  # noqa
    queryset = models.Chapter.objects.all()
    serializer_class = ChapterSerializer
    # permission_classes = (permissions.IsAuthenticated, )
