from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

class StudentAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            student = User.objects.get(email=email, is_student=True)
            if student.check_password(password):
                return student
        except User.DoesNotExist:
            return None

class LecturerAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            lecturer = User.objects.get(email=email, is_student=False)
            if lecturer.check_password(password):
                return lecturer
        except User.DoesNotExist:
            return None
