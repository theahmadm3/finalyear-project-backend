
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


class CreateStudentAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    timezone.activate('Africa/Lagos')
    def checkIfStudentLate(self,lecture_time, current_time):
        '''
        This checks if student is late within 30 mins from the lecture time
        '''
        current_hour = int(current_time.strftime("%H"))
        current_min=int(current_time.strftime("%M"))
        lecture_time_hour=int(lecture_time.strftime("%H"))
        lecture_time_min=int(lecture_time.strftime("%M"))
        if current_hour*60+current_min-(lecture_time_hour*60+current_min)<=32:
            return False
        return True

    def checkIfStudentRecordedAttendance(self,student_email,lecture_attendance_id):
        '''
        This  checks if student has recorded attendance within the time the  the lecture is initiated
        this is necessary to prevent duplicacy so that student don't create duplicate attendance at a for a particular
        lecture created at a particular time 
        '''
        attendance_record = StudentAttendance.objects.get(student_email=student_email,lecture_attendance=lecture_attendance_id)
        return attendance_record.exists()


    def createStudentAttendance(self,student_email,lecture_attendance_id):
        '''
        This creates the studentAttendance for the particular student
        '''
        StudentAttendance.objects.create(student_email=student_email, lecture_attendance_id=lecture_attendance_id)
        

    def post(self,request):
        if not request.user.is_student:
            return Response({"success":False,"message":"You are not a student"},status=400)
        student_email=request.data.get('email')
        lecture_attendance_id=request.data.get('lecture')
        time_lecture_created=LecturerAttendance.objects.get(id=lecture_attendance_id).timestamp
        time_lecture_created=timezone.localtime(time_lecture_created)
        current_time=timezone.localtime()
        if self.checkIfStudentLate(time_lecture_created, current_time):
            return Response({'success':False,'message':"you are late"},status=400)
            
        if self.checkIfStudentRecordedAttendance(self,student_email,lecture_attendance_id):
            return Response({'success':False,'message':'You have already Recorded Attendance'},status=400)
            
        CreateStudentAttendance(student_email,lecture_attendance_id)
        return Response({'success':True,'message':"Attendance recorded successfully"},status=200)
            
            
            
            
            
            


        
       


class CreateLecturerAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    timezone.activate('Africa/Lagos')
    def process_attendance(self, lecture, request_user,location,course_id):
        try:
            recent_attendance = LecturerAttendance.objects.filter(lecture=lecture, lecturer=request_user).latest('timestamp').timestamp
            recent_attendance= timezone.localtime(recent_attendance)
            time_frame = lecture.time_frame
            lecture_id=lecture.id

            if self.checkWithinInterval(recent_attendance, time_frame):
                qr_data = {"timestamp":recent_attendance.strftime('%H:%M:%S'),"timeframe":time_frame,"lat": lecture.location.split(' ')[0],"long":lecture.location.split(' ')[1],"course_id":lecture.course_id,'time':recent_attendance.strftime('%H:%M:%S'),'lecture_id':lecture_id}
                message = "You have already generated a QR code"
            else:
                lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
                
                qr_data = {"timestamp":lecturer_attendance.timestamp.strftime('%H:%M:%S'),"timeframe":time_frame,"lat": lecture.location.split(' ')[0],"course_id":lecture.course_id,'lecture_id':lecture_id}
                message = f"String for QR code"

        except LecturerAttendance.DoesNotExist:
            lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
            lecturer_attendance.save()
            time_frame = lecture.time_frame
            lecture_id=lecture.id
            qr_data = {"timestamp":lecturer_attendance.timestamp.strftime('%H:%M:%S') ,"timeframe":time_frame,"lat": lecture.location.split(' ')[0],"long":lecture.location.split(' ')[1],"course_id":lecture.course_id,'lecture_id':lecture_id}
            message = "String for QR code"

        except Exception as e:
            time_frame = lecture.time_frame
            return Response({'success': False, 'message': f'Error: from here {str(e)}', 'time_frame': time_frame}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'message': message, 
                         'data': qr_data})

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
        location = request.data.get('location')
        course_id=request.data.get('course')
        request.data['lecturer']=request.user.id

        if user.is_student:
            return Response({'success': False, 'message': 'Only a lecturer can start a lecture'}, status=status.HTTP_403_FORBIDDEN)
        
        if not self.checkWithinInterval(timezone.localtime(), time_frame):
            return Response({
                'success': False,
                'message': 'The time you are trying to create this lecture is not within bounds of the current time frame'
            },status=status.HTTP_400_BAD_REQUEST)

        serializer = LectureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        lecture, created = self.get_or_create_lecture(validated_data)
        return self.process_attendance(lecture, user,location,course_id)