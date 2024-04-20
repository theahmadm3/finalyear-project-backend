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
        return CustomUser.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"message":"Student data retrieved successfully","user": serializer.data,"success":True}, status=status.HTTP_200_OK)
