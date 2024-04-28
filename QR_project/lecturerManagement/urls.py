from django.contrib import admin
from django.urls import path
from .views import GetLecturerDetails,GetLecturerCourses


urlpatterns = [
    path('get/lecturer_courses',GetLecturerCourses.as_view(),name='lecturer_courses'),
    
]

