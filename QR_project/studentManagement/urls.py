from django.contrib import admin
from django.urls import path
from .views import GetStudentDetails,GetStudentCourses


urlpatterns = [
    path('get/student_courses',GetStudentCourses.as_view(),name='student_courses'),
    
]

