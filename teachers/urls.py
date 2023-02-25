from django.urls import path
from . import views


urlpatterns = [
    path('teachers/', views.TeacherListCreateAPIView.as_view()),
    path(
        'teachers/<int:pk>/', views.TeacherDetailUpdateDeleteAPIView.as_view()
    ),
    path('teachers/login/', views.teacher_login),

    path('categories/', views.CategoryListAPIView.as_view()),
]
