from django.urls import path
from . import views


urlpatterns = [
    path('', views.TeacherListCreateAPIView.as_view()),
    path(
        '<int:pk>/', views.TeacherDetailUpdateDeleteAPIView.as_view()
    ),
    path('teacher-login/', views.teacher_login),
]
