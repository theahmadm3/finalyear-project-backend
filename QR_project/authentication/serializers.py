# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class StudentTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        # Validate student credentials
        student = CustomUser.objects.filter(email=email, is_student=True).first()
        if student and student.check_password(password):
            return data
        else:
            raise serializers.ValidationError("Invalid student credentials")


class LecturerTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        # Validate lecturer credentials
        lecturer = CustomUser.objects.filter(email=email, is_student=False).first()
        if lecturer and lecturer.check_password(password):
            return data
        else:
            raise serializers.ValidationError("Invalid lecturer credentials")
