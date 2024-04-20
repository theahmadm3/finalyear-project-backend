from authentication.models  import CustomUser
from rest_framework import serializers

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['student_id', 'email','first_name','last_name','is_student','level','department','country','phone_number']  # Add any other fields you want to include