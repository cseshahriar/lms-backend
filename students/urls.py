from django.urls import path
from . import views


urlpatterns = [
    # teachers
    path('students/', views.StudentListCreateAPIView.as_view()),
    path(
        'students/<int:pk>/', views.StudentDetailUpdateDeleteAPIView.as_view()
    ),
    path('students/login/', views.StudentLoginAPIView.as_view()),
    path('students/password-reset/', views.PasswordChangeView.as_view()),

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
    # course favorites
    path('favorites/', views.StudentFavoriteCourseListAPIView.as_view()),
    path(
        'favorite_status/<int:course_id>/<int:student_id>/',
        views.course_favorite_status
    ),
    path(
        'remove_favorite_status/<int:course_id>/<int:student_id>/',
        views.remove_course_favorite
    ),
    # course rating
    path(
        'course-rating/',
        views.CourseRatingListCreateAPIView.as_view()
    ),
    path(
        'rating_status/<int:course_id>/<int:student_id>/',
        views.rating_status
    ),
    # StudentAssignment
    path(
        'assignments/', views.StudentAssignmentListCreateAPIView.as_view()
    ),
    path(
        'assignments/<int:pk>', views.StudentAssignmentDetailAPIView.as_view()
    )
]
