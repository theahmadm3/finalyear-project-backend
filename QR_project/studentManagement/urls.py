from django.contrib import admin
from django.urls import path
from .views import GetStudentDetails,GetStudentCourses


urlpatterns = [
    path('get/student',GetStudentDetails.as_view(),name='login_stud'),
    path('get/student_courses',GetStudentCourses.as_view(),name='student_courses'),
    
]

