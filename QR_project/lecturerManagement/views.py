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
                                 'teaching': data_serialized.data,
                                 'success': True})
            else:
                return Response({'message': 'No courses found for the lecturer',
                                 'teaching': [],
                                 'success': False})
        except Exception as e:
            return Response({'message': 'Error', 
                             'teaching': f"Error message: {e}",
                             'success': False})


class GetLecturerDetails(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = lecturerUserSerializer

    def get_object(self):
        try:
            # Retrieve the lecturer user if exists
            return CustomUser.objects.get(id=self.request.user.id, is_student=False)
        except CustomUser.DoesNotExist:
            # Return None if the lecturer is not found
            return None

    def retrieve(self, request, *args, **kwargs):
        lecturer = self.get_object()

        if lecturer is not None:
            serializer = self.get_serializer(lecturer)
            return Response({"message": "Lecturer data retrieved successfully", "user": serializer.data, "success": True}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Lecturer not found", "success": False}, status=status.HTTP_404_NOT_FOUND)
# Create your views here.
