from rest_framework import serializers
from authentication.models import CustomUser
from courseManagement.models import Course
from .models import StudentCourses

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

class CourseSerializer(serializers.ModelSerializer):
    lecturer = CustomUserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['student_id', 'email', 'first_name', 'last_name', 'is_student', 'level', 'department', 'country', 'phone_number']

class StudentCoursesSerializer(serializers.ModelSerializer):
    course_details =CourseSerializer()  # Nested serializer for the Course model
    #student = CustomUserSerializer()  # Nested serializer for the CustomUser model

    class Meta:
        model = StudentCourses
        fields = ['course_details']