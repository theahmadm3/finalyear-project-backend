from django.contrib import admin
from django.urls import path
from .views import GetStudentDetails,GetStudentCourses,GetEnrolledStudents


urlpatterns = [
    path('get/student_courses',GetStudentCourses.as_view(),name='student_courses'),
    path('get/enrolled_student/<int:course_id>',GetEnrolledStudents.as_view(),name='student_courses'),
    
]

