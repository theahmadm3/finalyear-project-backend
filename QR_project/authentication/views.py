from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import StudentTokenObtainPairSerializer, LecturerTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import LecturerUSerSerializer, StudentUserSerializer

class StudentTokenObtainPairView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            # Customize the success response here if needed
            custom_data = {'message': 'Login successful',
                           'success': True}
            custom_data.update(response.data)
            return Response(custom_data, status=status.HTTP_200_OK)
        except Exception as e:
            return self.handle_exception(e)

    def handle_exception(self, exc):
        # Customize the error response here
        response_data = {'error': 'An error occurred during login',
                         'success':False
                         ,'message':str(exc)}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class LecturerTokenObtainPairView(TokenObtainPairView):
    serializer_class = LecturerTokenObtainPairSerializer



class CreateUser(APIView):
    def post(self, request):
        is_student = request.data.get('is_student', None)
        if is_student is None:
            return Response({'success': False, 'message': 'Please Add the is_student'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer_class = StudentUserSerializer if is_student else LecturerUserSerializer
        serializer = serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        errors = {}
        for field, messages in serializer.errors.items():
            errors[field] = ', '.join(messages)
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)