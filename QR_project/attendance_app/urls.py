from django.contrib import admin
from django.urls import path
from .views import CreateLecturerAttendance


urlpatterns = [
    path('create/lecturer/attendance',CreateLecturerAttendance.as_view(),name='lecturer_attendance'),    
]

