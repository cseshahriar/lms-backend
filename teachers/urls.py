from django.urls import path
from . import views


urlpatterns = [
    # teachers
    path('teachers/', views.TeacherListCreateAPIView.as_view()),
    path(
        'teachers/<int:pk>/', views.TeacherDetailUpdateDeleteAPIView.as_view()
    ),
    path('teachers/login/', views.TeacherLoginAPIView.as_view()),
    # path('teachers/login/', views.teacher_login),

    # categories
    path('categories/', views.CategoryListAPIView.as_view()),

    # courses
    path('courses/', views.CourseListCreateAPIView.as_view()),
    path(
        'courses/<int:pk>/',
        views.CourseRetrieveUpdateDeleteAPIView.as_view()
    ),
    path(
        'teacher/<int:teacher_id>/courses/',
        views.TeacherCourseListAPIView.as_view()
    ),
    path(
        'courses/<int:course_id>/chapters/',
        views.ChapterListCreateAPIView.as_view()
    ),
    path(
        'chapters/<int:pk>/',
        views.ChapterRetrieveUpdateDeleteAPIView.as_view()
    ),
]
