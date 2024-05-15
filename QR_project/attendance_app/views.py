
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
from .serializers import LectureSerializer,LecturerAttendanceSerializer,StudentAttendanceSerializer
from django.utils import timezone
import re
import json
class LecturerCreateStudentAtttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['student_ids', 'lecture_attendance_id'],
            properties={
                'student_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                'lecture_attendance_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )
    def post(self, request):
        if request.user.is_student:
            return Response({'success':False,'message':'Only a Lecturer can do this'},status=400)
        def create_student_attendance(student_id, lecture_attendance_id):
            try:
                student_attendance = StudentAttendance.objects.get(student_id=student_id, lecture_attendance=lecture_attendance_id)
                return False  # Attendance already exists
            except StudentAttendance.DoesNotExist:
                StudentAttendance.objects.create(student_id=student_id, lecture_attendance_id=lecture_attendance_id)
                return True  # Attendance created successfully

        try:
            data = json.loads(request.body)
            student_ids = data.get('student_ids', [])
            lecture_attendance_id = data.get('lecture_attendance_id')

            if isinstance(student_ids, list) and all(isinstance(item, int) for item in student_ids):
                successes = []
                for student_id in student_ids:
                    success = create_student_attendance(student_id, lecture_attendance_id)
                    if success:
                        successes.append(student_id)

                return Response({'success': True, 'message': 'Student Attendance created successfully'},status=200)
            else:
                return Response({'error': 'Invalid input. Expecting an array of integers.'}, status=400)
        except Exception as e:
            return Response({'error':str(e)}, status=400)

class ViewStudentThatAttendedLecture(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if  request.user.is_student:
            return Response({'success':False,
                             'message':'Student can not access these records'},status=400)
        else:
            lectureAttendanceId = kwargs['lecture_attendance_id']
            try:
                attendanceRecord = StudentAttendance.objects.filter(lecture_attendance=lectureAttendanceId)
                if attendanceRecord.exists():
                    serializer = StudentAttendanceSerializer(instance=attendanceRecord, many=True)
                    return Response({'success':True,
                                    'message':'Successfully retrieved',
                                    'data':serializer.data},status=200)
                else:
                    return Response({'success':False,
                                  'message':'No student attended this Lecture'},status=400)



            except Exception as e:
                return Response({'success':False,
                                  'message':str(e)},status=400)
        



class GetLecturerAttendancesForCourses(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        if  not request.user.is_student:
            course_id=kwargs['course_id']
            filltered_attendances=LecturerAttendance.objects.filter(lecture__course=course_id)
            if filltered_attendances.exists():
                serializer=LecturerAttendanceSerializer(instance=filltered_attendances, many=True)
                return Response({'success':True,'message':'Successfuly retrieved','data':serializer.data})
            else:
                return Response({'success':False,'message':'You did any lecture for this course'})
            
        else:
            return Response({'success':False,'message':'You are not a lecturer'},status=400)

        


class GetStudentAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['course_id'],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )   
    def post(self, request):
        try: 
           student=request.user
           course_id=request.data.get('course_id')

           filtered_student_attendance_count = StudentAttendance.objects.filter(student=student,lecture_attendance__lecture__course_id=course_id).count()
           filtered_lecturer_attendance_count = LecturerAttendance.objects.filter(lecture__course=course_id).count()
           if filtered_lecturer_attendance_count==0:score=0 
           else:score=int(filtered_student_attendance_count/filtered_lecturer_attendance_count *100)

           return Response({'success':True,
                             'message':'Attendance retrieved successfully',
                             'data':score},status=200)
        except Exception as e:
            return Response({'success':False,'message':str(e)},status=400)  


class CreateStudentAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    timezone.activate('Africa/Lagos')
    def checkIfStudentLate(self,lecture_time, current_time):
        '''
        This checks if student is late within 30 mins from the lecture time
        '''
        current_datetime = current_time.replace(second=0, microsecond=0)  # Ensure seconds and microseconds are zeroed
        lecture_datetime = lecture_time.replace(second=0, microsecond=0)  # Ensure seconds and microseconds are zeroed

        time_difference = current_datetime - lecture_datetime
        total_minutes_difference = abs(time_difference.days * 24 * 60 + time_difference.seconds // 60)

        if total_minutes_difference <= 30:
            return False
        return True

    def checkIfStudentRecordedAttendance(self,student,lecture_attendance_id):
        '''
        This  checks if student has recorded attendance within the time the  the lecture is initiated
        this is necessary to prevent duplicacy so that student don't create duplicate attendance at a for a particular
        lecture created at a particular time 
        '''
        try:
           attendance_record=StudentAttendance.objects.get(student=student,lecture_attendance=lecture_attendance_id)
           return True
        except StudentAttendance.DoesNotExist:
            return False
        


    def createStudentAttendance(self,student,lecture_attendance_id):
        '''
        This creates the studentAttendance for the particular student
        '''
        StudentAttendance.objects.create(student=student, lecture_attendance_id=lecture_attendance_id)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['lecture'],
            properties={
                'lecture': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )   

    def post(self,request):
        if not request.user.is_student:
            return Response({"success":False,"message":"You are not a student"},status=400)
        student=request.user
        lecture_attendance_id=request.data.get('lecture')

        time_lecture_created=LecturerAttendance.objects.get(id=lecture_attendance_id).timestamp
        time_lecture_created=timezone.localtime(time_lecture_created)
        current_time=timezone.localtime()

        if self.checkIfStudentLate(time_lecture_created, current_time):
            return Response({'success':False,'message':"you are late"},status=400)
            
        if self.checkIfStudentRecordedAttendance(student,lecture_attendance_id):
            return Response({'success':False,'message':'You have already Recorded Attendance'},status=400)
            
        self.createStudentAttendance(student,lecture_attendance_id)
        return Response({'success':True,'message':"Attendance recorded successfully"},status=200)
            

class CreateLecturerAttendance(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    timezone.activate('Africa/Lagos')
    def process_attendance(self, lecture, request_user,location,course_id):
        try:
            recent_attendance = LecturerAttendance.objects.filter(lecture=lecture, lecturer=request_user).latest('timestamp')
            recent_attendance_time= timezone.localtime(recent_attendance.timestamp)
            time_frame = lecture.time_frame
            lecture_id=recent_attendance.id

            if self.checkWithinInterval(recent_attendance_time, time_frame):
                qr_data = {"timestamp":recent_attendance_time.strftime('%H:%M:%S'),"timeframe":time_frame,"lat": location.split(' ')[0],"long":location.split(' ')[1],"course_id":lecture.course_id,'lecture_id':lecture_id}
                message = "You have already generated a QR code"
            else:
                lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
                
                qr_data = {"timestamp":lecturer_attendance.timestamp.strftime('%H:%M:%S'),"timeframe":time_frame,"lat": location.split(' ')[0],"long":location.split(' ')[1],"course_id":lecture.course_id,'lecture_id':lecturer_attendance.id}
                message = f"String for QR code"

        except LecturerAttendance.DoesNotExist:
            lecturer_attendance = LecturerAttendance.objects.create(lecture=lecture, lecturer=request_user)
            lecturer_attendance.save()
            time_frame = lecture.time_frame
            lecture_id=lecturer_attendance.id
            qr_data = {"timestamp":lecturer_attendance.timestamp.strftime('%H:%M:%S') ,"timeframe":time_frame,"lat":location.split(' ')[0],"long":location.split(' ')[1],"course_id":lecture.course_id,'lecture_id':lecture_id}
            message = "String for QR code"

        except Exception as e:
            time_frame = lecture.time_frame
            return Response({'success': False, 'message': f'Error: from here {str(e)}', 'time_frame': time_frame}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': True, 'message': message, 
                         'data': qr_data})

    def checkWithinInterval(self, recent_time, time_frame):
        start_hour, end_hour = map(int, time_frame.split('-'))
        
        current_hour = int(recent_time.strftime("%H"))
        return start_hour <= current_hour < end_hour

    def get_or_create_lecture(self, validated_data):
        lectures = Lecture.objects.filter(
            course=validated_data.get('course'),
            #location=validated_data.get('location'),
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
        location_value = request.data.pop('location', None)
        
        serializer = LectureSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        lecture, created = self.get_or_create_lecture(validated_data)
        return self.process_attendance(lecture, user,location,course_id)