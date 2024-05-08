from django.contrib import admin
from django.urls import path
from .views import CreateLecturerAttendance, CreateStudentAttendance


urlpatterns = [
    path('create/lecturer/attendance',CreateLecturerAttendance.as_view(),name='lecturer_attendance'),    
    path('create/student/attendance',CreateStudentAttendance.as_view(),name='student_attendance'),    
]

