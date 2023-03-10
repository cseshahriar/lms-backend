from django.urls import path
from . import views


urlpatterns = [
    # teachers
    path('students/', views.StudentListCreateAPIView.as_view()),
    path(
        'students/<int:pk>/', views.StudentDetailUpdateDeleteAPIView.as_view()
    ),
    path('students/login/', views.StudentLoginAPIView.as_view()),
    # enrollment
    path('enrollments/', views.StudentEnrollmentListCreateAPIView.as_view()),
    path(
        'enrollment_status/<int:course_id>/<int:student_id>/',
        views.enrollment_status
    ),
    path(
        'enrollments/courses/<int:course_id>/',
        views.EnrolledStudentListAPIView.as_view()
    ),
]
