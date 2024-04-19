from django.contrib import admin
from django.urls import path
from .views import StudentTokenObtainPairView,LecturerTokenObtainPairView


urlpatterns = [
    path('login/student',StudentTokenObtainPairView.as_view(),name='login_stud'),
    path('login/lecturer',LecturerTokenObtainPairView.as_view(),name='login_lec'),  
]

