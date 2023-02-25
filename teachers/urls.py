from django.urls import path
from . import views


urlpatterns = [
    # teachers
    path('teachers/', views.TeacherListCreateAPIView.as_view()),
    path(
        'teachers/<int:pk>/', views.TeacherDetailUpdateDeleteAPIView.as_view()
    ),
    path('teachers/login/', views.teacher_login),

    # categories
    path('categories/', views.CategoryListAPIView.as_view()),

    # courses
    path('courses/', views.CourseListCreateAPIView.as_view()),
]
