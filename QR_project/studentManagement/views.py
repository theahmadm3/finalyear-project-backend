from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from authentication.models  import CustomUser
from .serializers import StudentUserSerializer

class GetStudentDetails(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
