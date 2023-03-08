from django.urls import path
from . import views


urlpatterns = [
    # teachers
    path('students/', views.StudentListCreateAPIView.as_view()),
    path(
        'students/<int:pk>/', views.StudentDetailUpdateDeleteAPIView.as_view()
    ),
    path('students/login/', views.StudentLoginAPIView.as_view()),
]