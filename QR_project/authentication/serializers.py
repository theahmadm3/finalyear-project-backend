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
        



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_student = serializers.BooleanField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_student', 'username', 'first_name', 'last_name', 'level', 'department', 'country', 'phone_number','student_id']
    
    
    def create(self, validated_data):
        # Extract the password from the validated data
        password = validated_data.pop('password', None)
        # Create a new user instance with the remaining validated data
        user = CustomUser.objects.create(**validated_data)
        # Set the password for the user
        if password:
            user.set_password(password)
            user.save()
        return user