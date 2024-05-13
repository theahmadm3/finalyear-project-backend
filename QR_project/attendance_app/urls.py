from django.contrib import admin
from django.urls import path
from .views import CreateLecturerAttendance, CreateStudentAttendance,GetStudentAttendance,GetLecturerAttendancesForCourses


urlpatterns = [
    path('create/lecturer/attendance',CreateLecturerAttendance.as_view(),name='lecturer_attendance'),    
    path('create/student/attendance',CreateStudentAttendance.as_view(),name='student_attendance'),    
    path('get/student/attendance',GetStudentAttendance.as_view(),name='student_attendance'),    
    path('get/Lecturer/attendance/<int:course_id>',GetLecturerAttendancesForCourses.as_view(),name='student_attendance'),    
]

