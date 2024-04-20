from django.contrib import admin
from django.urls import path
from .views import GetStudentDetails


urlpatterns = [
    path('get/student',GetStudentDetails.as_view(),name='login_stud'),
    
]

