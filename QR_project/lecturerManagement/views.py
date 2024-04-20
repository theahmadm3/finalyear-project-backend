from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from authentication.models  import CustomUser
from .serializers import lecturerUserSerializer,LecturerCoursesSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from courseManagement.models import Course



class GetLecturerCourses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            lecturer = request.user
            lecturer_courses =  Course.objects.filter(lecturer=lecturer)
            # Ensure the queryset contains multiple objects
            if lecturer_courses.exists():
                # Pass the queryset instance to the serializer
                data_serialized = LecturerCoursesSerializer(instance=lecturer_courses, many=True)
                return Response({'message': "lecturer courses retrieved successfully",
                                 'enrolled': data_serialized.data,
                                 'success': True})
            else:
                return Response({'message': 'No courses found for the lecturer',
                                 'enrolled': [],
                                 'success': False})
        except Exception as e:
            return Response({'message': 'Error', 
                             'enrolled': f"Error message: {e}",
                             'success': False})


class GetLecturerDetails(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = lecturerUserSerializer

    def get_queryset(self):
        return CustomUser.objects.get(id=self.request.user.id,is_student=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response({"message":"Lecturer data retrieved successfully","user": serializer.data,"success":True}, status=status.HTTP_200_OK)

# Create your views here.
