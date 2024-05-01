from .models import Lecture
from rest_framework import serializers


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields =['course','location','time_frame']
