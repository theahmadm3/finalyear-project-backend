from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from authentication.models  import CustomUser
from .serializers import StudentUserSerializer,StudentCoursesSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentCourses



class GetStudentCourses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            student = request.user
            student_courses = StudentCourses.objects.filter(student=student)
            # Ensure the queryset contains multiple objects
            if student_courses.exists():
                # Pass the queryset instance to the serializer
                data_serialized = StudentCoursesSerializer(instance=student_courses, many=True)
                return Response({'message': "Student courses retrieved successfully",
                                 'enrolled': data_serialized.data,
                                 'success': True})
            else:
                return Response({'message': 'No courses found for the student',
                                 'enrolled': [],
                                 'success': False})
        except Exception as e:
            return Response({'message': 'Error', 
                             'enrolled': f"Error message: {e}",
                             'success': False})


class GetStudentDetails(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentUserSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        try:
            # Fetch the user based on authentication and whether they are a student
            return CustomUser.objects.get(id=user_id, is_student=True)
        except CustomUser.DoesNotExist:
            # If the user is not found or not a student, return None
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is not None:
            try:
                serializer = self.get_serializer(queryset)
                # Return student data if found
                return Response({"message": "Student data retrieved successfully", 
                                 "user": serializer.data, "success": True}, 
                                status=status.HTTP_200_OK)
            except Exception as e:
                # Return error message if serialization fails
                return Response({"message": str(e), "success": False}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return error message if user is not found or not a student
            return Response({"message": "User not found or not a student", 
                             "success": False}, status=status.HTTP_404_NOT_FOUND)
