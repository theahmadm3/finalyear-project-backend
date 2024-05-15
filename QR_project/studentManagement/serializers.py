from rest_framework import serializers
from authentication.models import CustomUser
from courseManagement.models import Course
from .models import StudentCourses

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']

class CourseSerializer(serializers.ModelSerializer):
    lecturer = CustomUserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','student_id', 'email', 'first_name', 'last_name', 'is_student', 'level', 'department', 'country', 'phone_number']
        ref_name = 'StudentManagementStudentUserSerializer'

class StudentCoursesSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer()  # Nested serializer for the Course model

    class Meta:
        model = StudentCourses
        fields = ['course_details']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove the "course_details" wrapper and flatten the representation
        course_data = representation.pop('course_details')
        # Move the lecturer's email directly under the course data
        course_data['email'] = course_data['lecturer']['email']
        course_data['first_name'] = course_data['lecturer']['first_name']
        course_data['last_name'] = course_data['lecturer']['last_name']
        # Remove the lecturer key from course_data
        del course_data['lecturer']
        # Merge the modified course_data into the representation
        representation.update(course_data)
        return representation


class EnrolledStudentSerializer(serializers.ModelSerializer):
    student=StudentUserSerializer() # Nested serializer for the Course model

    class Meta:
        model = StudentCourses
        fields = ['student']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        student_details=representation.pop('student')
        representation['id']=student_details['id']
        representation['first_name']=student_details['first_name']
        representation['last_name']=student_details['last_name']
        representation['student_id']=student_details['student_id']
        return representation

