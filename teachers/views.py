from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import (
    TeacherSerializer, CourseCategorySerializer, CourseSerializer)
from . import models


class TeacherListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = (permissions.IsAuthenticated, )


class TeacherDetailUpdateDeleteAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (permissions.IsAuthenticated, )


@csrf_exempt
@api_view(['POST'])
def teacher_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        teacher = models.Teacher.objects.filter(
            email=email, password=password
        ).first()
        if teacher:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})


class CategoryListAPIView(generics.ListAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    # permission_classes = (permissions.IsAuthenticated, )


class CourseListCreateAPIView(generics.ListCreateAPIView):
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
