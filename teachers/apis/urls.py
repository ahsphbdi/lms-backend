from django.urls import path
from .views import TeacherCourseDetailAPIView, TeacherCourseStudentSettingAPIView, \
    TeacherSessionDetailAPIView, TeacherHomeAPIView


urlpatterns = [
    path('home/', TeacherHomeAPIView.as_view(), name="home"),
    path('course/<int:course_id>/',
         TeacherCourseDetailAPIView.as_view(), name="course_detail"),
    path('session/<int:course_id>/',
         TeacherSessionDetailAPIView.as_view(), name="course_detail"),
    path('course/<int:course_id>/setting/students/', TeacherCourseStudentSettingAPIView.as_view(),
         name="student_setting")
]
