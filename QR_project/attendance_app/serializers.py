from .models import Lecture, LecturerAttendance,StudentAttendance
from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from authentication.models import CustomUser



class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [ 'id','first_name', 'last_name', 'student_id']


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student=StudentUserSerializer()
    class Meta:
        model=StudentAttendance
        fields=['student']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Remove the "course_details" wrapper and flatten the representation
        student_data = representation.pop('student')
        # Move the lecturer's email directly under the course data
        representation['id'] = student_data['id']
        representation['first_name'] = student_data['first_name']
        representation['last_name'] = student_data['last_name']
        representation['student_id'] = student_data['student_id']
        return representation
    


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields ='__all__'

class MyLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields =['time_frame']

class LecturerAttendanceSerializer(serializers.ModelSerializer):
    lecture=LectureSerializer()
    class Meta:
        model=LecturerAttendance
        fields=['id','lecture','timestamp']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Remove the "course_details" wrapper and flatten the representation
        lecture_data = representation.pop('lecture')
        # Move the lecturer's email directly under the course data
        representation['id'] = lecture_data['id']
        representation['time_frame'] = lecture_data['time_frame']
        time_str=representation['timestamp']
        time = datetime.fromisoformat(time_str)
        local_time=timezone.localtime(time)
        date=local_time.strftime("%dth %B %Y")
        representation['timestamp']=date

        # Remove the lecturer key from lecture_data
        # Merge the modified lecture_data into the representation
        return representation
