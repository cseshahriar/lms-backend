from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.views.decorators import csrf_exempt
from django.http import JsonResponse


from .serializers import TeacherSerializer
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


def teacher_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    teacher = models.Teacher.objects.get(email=email, password=password)
    if teacher:
        return JsonResponse({'bool': True})
    else:
        return JsonResponse({'bool': False})
