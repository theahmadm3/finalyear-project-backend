from django.contrib import admin
from django.urls import path
from .views import StudentTokenObtainPairView,LecturerTokenObtainPairView,CreateUser,GetUserDetails,GetUserDetails


urlpatterns = [
    path('login/student',StudentTokenObtainPairView.as_view(),name='login_stud'),
    path('login/lecturer',LecturerTokenObtainPairView.as_view(),name='login_lec'),  
    path('create/user',CreateUser.as_view(),name='create_user'),  
    path('get/user',GetUserDetails.as_view(),name='get_user'),  
]

