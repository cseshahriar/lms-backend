from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view


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


@csrf_exempt
@api_view(['POST'])
def teacher_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print('-', 'data', email, password)
        teacher = models.Teacher.objects.filter(email=email).first()
        print('-' * 30, 'teachers', teacher)
        if teacher:
            return JsonResponse({'bool': True})
        else:
            return JsonResponse({'bool': False})
