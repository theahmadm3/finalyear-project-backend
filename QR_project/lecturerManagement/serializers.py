
from rest_framework import serializers
from authentication.models import CustomUser
from courseManagement.models import Course


class lecturerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','department','country','phone_number']


class LecturerCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','title','course_code']

    