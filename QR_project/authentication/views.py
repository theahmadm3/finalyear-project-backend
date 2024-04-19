from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import StudentTokenObtainPairSerializer, LecturerTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class StudentTokenObtainPairView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer

class LecturerTokenObtainPairView(TokenObtainPairView):
    serializer_class = LecturerTokenObtainPairSerializer
