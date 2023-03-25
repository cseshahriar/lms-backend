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
    StudentSerializer, StudentCourseEnrolmentSerializer,
    CourseRatingSerializer, StudentPasswordChangeSerializer,
    StudentFavoriteCourseSerializer
)
from .models import (
    Student, StudentCourseEnrolment, CourseRating, StudentFavoriteCourse)


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


class PasswordChangeView(APIView):
    """ password change api view"""
    def post(self, request, format=None):
        serializer = StudentPasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            pk = serializer.validated_data.get('pk')
            new_password = serializer.validated_data.get('new_password')
            user = Student.objects.filter(pk=pk).first()
            password = make_password(new_password)
            user.password = password
            user.save()
            return Response({'message': 'Password changed successfully.'})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class StudentEnrollmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudentCourseEnrolment.objects.all()
    serializer_class = StudentCourseEnrolmentSerializer
    # permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = super().get_queryset()

        # return course_id by teacher
        if 'course_id' in self.request.GET:
            course_id = int(self.request.GET.get('course_id'))
            qs = qs.filter(
                course_id=course_id
            ).order_by('-id')

        # return students by teacher
        if 'student_id' in self.request.GET:
            student_id = int(self.request.GET.get('student_id'))
            qs = qs.filter(
                student_id=student_id
            ).order_by('-id')

        if 'studentId' in self.request.GET:  # return recommended course
            student_id = int(self.request.GET.get('studentId'))
            student = Student.objects.get(id=student_id)
            interested_categories = [
                x.lower().strip()
                for x in student.interested_categories.split(',')
            ]
            qs = qs.filter(
                course__technologies__in=interested_categories
            ).distinct()

        # return course by teacher
        if 'teacher_id' in self.request.GET:
            teacher_id = int(self.request.GET.get('teacher_id'))
            qs = qs.filter(
                course__teacher_id=teacher_id
            ).distinct('student')

        return qs


@api_view(['GET'])
def enrollment_status(request, course_id, student_id):
    if StudentCourseEnrolment.objects.filter(
        course_id=course_id, student_id=student_id
    ).exists():
        return JsonResponse({'bool': True})
    return JsonResponse({'bool': False})


class EnrolledStudentListAPIView(generics.ListAPIView):
    queryset = StudentCourseEnrolment.objects.all()
    serializer_class = StudentCourseEnrolmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.kwargs['course_id']
        print('-' * 30, 'data', course_id)
        return qs.filter(course_id=course_id)


class StudentFavoriteCourseListAPIView(generics.ListCreateAPIView):
    queryset = StudentFavoriteCourse.objects.all()
    serializer_class = StudentFavoriteCourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        # return course_id by teacher
        if 'course_id' in self.request.GET:
            course_id = int(self.request.GET.get('course_id'))
            qs = qs.filter(
                course_id=course_id
            ).order_by('-id')

        # return students by teacher
        if 'student_id' in self.request.GET:
            student_id = int(self.request.GET.get('student_id'))
            qs = qs.filter(
                student_id=student_id
            ).order_by('-id')

        return qs


@api_view(['GET'])
def course_favorite_status(request, course_id, student_id):
    if StudentFavoriteCourse.objects.filter(
        course_id=course_id, student_id=student_id
    ).exists():
        return JsonResponse({'bool': True})
    return JsonResponse({'bool': False})


class CourseRatingListCreateAPIView(generics.ListCreateAPIView):
    queryset = CourseRating.objects.all()
    serializer_class = CourseRatingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs.get('course_id', None) is not None:
            course_id = self.kwargs['course_id']
            return qs.filter(course_id=course_id)

        if self.kwargs.get('student_id', None) is not None:
            student_id = self.kwargs['student_id']
            return qs.filter(student_id=student_id)

        return qs


@api_view(['GET'])
def rating_status(request, course_id, student_id):
    if CourseRating.objects.filter(
        course_id=course_id, student_id=student_id
    ).exists():
        return JsonResponse({'bool': True})
    return JsonResponse({'bool': False})
