from authentication.models  import CustomUser
from . models import StudentCourses
from authentication.models import CustomUser
from courseManagement.models import Course

from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        mode=CustomUser
        fields = ['email']

class CourseSerializer(serializers.ModelSerializer):
    lecturer=CustomUserSerializer(read_only=True)
    class Meta:
        model=Course
        fields='__all__'



class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['student_id', 'email','first_name','last_name','is_student','level','department','country','phone_number']
        
        
        
        

class StudentCoursesSerializer(serializers.ModelSerializer):
    enrolled = CourseSerializer(many=True,read_only=True)  # Nested serializer for Course
    student = CustomUserSerializer(read_only=True)  # Nested serializer for CustomUser

    class Meta:
        model = StudentCourses
        fields = '__all__'  # Include all fields in the serialized output
  # Add any other fields you want to include