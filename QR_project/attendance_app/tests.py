from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from .models import Lecture, LecturerAttendance, StudentAttendance
from django.utils import timezone


class AttendanceTestCase(APITestCase):
    def setUp(self):
        # Create a user with student role
        self.student_user = User.objects.create_user(username='student', password='password', is_student=True)
        # Create a user with lecturer role
        self.lecturer_user = User.objects.create_user(username='lecturer', password='password', is_lecturer=True)
        # Create a lecture
        self.lecture = Lecture.objects.create(
            course="Sample Course",
            location="Sample Location",
            time_frame="10-11",
            lecturer=self.lecturer_user
        )
        # Create JWT access tokens for authentication
        self.student_token = AccessToken.for_user(self.student_user)
        self.lecturer_token = AccessToken.for_user(self.lecturer_user)

    def test_create_student_attendance(self):
        url = reverse('create_student_attendance')  # Assuming you have a proper URL configuration
        data = {'lecture': self.lecture.id}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lecturer_attendance(self):
        url = reverse('create_lecturer_attendance')  # Assuming you have a proper URL configuration
        data = {
            'course': 'Sample Course',
            'location': 'Sample Location',
            'time_frame': '10-11'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.lecturer_token}')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

