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
from .serializers import (
    TeacherSerializer, CourseCategorySerializer, CourseSerializer,
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
    serializer_class = TeacherSerializer
    permission_classes = (permissions.IsAuthenticated, )

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
                status=status.HTTP_401_UNAUTHORIZED
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
        if 'limit' in self.request.GET:
            limit = int(self.request.GET.get('limit'))
            qs = models.Course.objects.all().order_by('-id')[:limit]
            print('-' * 30, 'qs', qs)
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
