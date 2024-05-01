
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .models import Lecture,StudentAttendance,LecturerAttendance
from datetime import datetime
from .serializers import LectureSerializer
from django.utils import timezone
import re

class CreateLecturerAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    timezone.activate('Africa/Lagos')
    def process_attendance(self, lecture, request_user):
        try:
            recent_attendance = LecturerAttendance.objects.filter(lecture=lecture, lecturer=request_user).latest('timestamp').timestamp
            time_frame = lecture.time_frame

            if self.checkWithinInterval(recent_attendance, time_frame):
                qr_data = f"{recent_attendance}_{time_frame}_{lecture.location}_{lecture.course_id}"
                message = "You have already generated a QR code"
            else:
                lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
                qr_data = f"{lecturer_attendance.timestamp}_{time_frame}_{lecture.location}_{lecture.course_id}_exist"
                message = "String for QR code"

        except LecturerAttendance.DoesNotExist:
            lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
            lecturer_attendance.save()
            time_frame = lecture.time_frame
            qr_data = f"{lecturer_attendance.timestamp}_{time_frame}_{lecture.location}_{lecture.course_id}_does not exist"
            message = "String for QR code"

        except Exception as e:
            time_frame = lecture.time_frame
            return Response({'success': False, 'message': f'Error: {str(e)}', 'time_frame': time_frame}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'message': message, 
                         'data': qr_data,'time':timezone.now()})

    def checkWithinInterval(self, recent_time, time_frame):
        start_hour, end_hour = map(int, time_frame.split('-'))
        current_hour = int(recent_time.strftime("%H"))
        return recent_time.date() == timezone.now().date() and start_hour <= current_hour <= end_hour

    def get_or_create_lecture(self, validated_data):
        lectures = Lecture.objects.filter(
            course=validated_data.get('course'),
            location=validated_data.get('location'),
            time_frame=validated_data.get('time_frame'),
            lecturer=validated_data.get('lecturer')
        )
        if lectures.exists():
            return lectures.first(), False
        else:
            return Lecture.objects.create(**validated_data), True

    @swagger_auto_schema(request_body=LectureSerializer)
    def post(self, request):
        user = request.user
        time_frame = request.data.get('time_frame')

        if user.is_student:
            return Response({'success': False, 'message': 'Only a lecturer can start a lecture'}, status=status.HTTP_403_FORBIDDEN)
        
        if not self.checkWithinInterval(timezone.localtime(), time_frame):
            return Response({
                'success': False,
                'message': 'The time you are trying to create this lecture is not within bounds of the current time frame'
            })

        serializer = LectureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        lecture, created = self.get_or_create_lecture(validated_data)

        if not created:
            serializer.instance = lecture

        lecture = serializer.save()

        return self.process_attendance(lecture, user)