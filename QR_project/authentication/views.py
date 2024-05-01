from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import StudentTokenObtainPairSerializer, LecturerTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from studentManagement.serializers import StudentUserSerializer
from lecturerManagement.serializers import lecturerUserSerializer 

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
    @swagger_auto_schema(request_body=CustomUserSerializer)

    def post(self, request):
        # Get is_student field from request data
        is_student = request.data.get('is_student', None)
        if is_student is None:
            return Response({'success': False, 'message': 'Please Add the is_student field'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create serializer instance
        serializer = CustomUserSerializer(data=request.data)
        
        # Validate serializer data
        if serializer.is_valid():
            # Save the user
            serializer.save(is_student=is_student)
            return Response({'success':True,
                             'message':'User created successfully'}, status=status.HTTP_201_CREATED)
        
        # If validation fails, return errors
        errors = serializer.errors
        return Response({'success':False,
                         'message':'User not created successfully',
                        'errors': errors}, status=status.HTTP_400_BAD_REQUEST)



class GetUserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user=request.user
            if user.is_student:
                serialized=StudentUserSerializer(user)
                return Response({
                    'success':True,
                    'message':'student retrieved successfully',
                    'data':serialized.data
                })
            
            else:
                serialized=lecturerUserSerializer(user)
                return Response({
                    'success':True,
                    'message':'Lecturer retrieved successfully',
                    'data':serialized.data
                })
        except Exception as e:
            return Response({'success':False, 'message':str(e)})
                


