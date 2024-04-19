import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QR_project.settings')
django.setup()# Configure Django settings
settings.configure()
from django.contrib.auth import get_user_model

User = get_user_model()

def create_users():
    # Dummy data for creating users
    lecturer_data = [
        {"email": "lecturer1@example.com", "password": "password1", "username": "lecturer1", "first_name": "John", "last_name": "Doe"},
        {"email": "lecturer2@example.com", "password": "password2", "username": "lecturer2", "first_name": "Jane", "last_name": "Smith"},
        {"email": "lecturer3@example.com", "password": "password3", "username": "lecturer2", "first_name": "Jane", "last_name": "Smith"},
        # Add more dummy data as needed
    ]

    student_data = [
        {"email": "student1@example.com", "password": "password1", "username": "student1", "first_name": "Alice", "last_name": "Johnson"},
        {"email": "student2@example.com", "password": "password2", "username": "student2", "first_name": "Bob", "last_name": "Brown"},
        # Add more dummy data as needed
    ]

    # Create lecturers
    for data in lecturer_data:
        User.objects.create_lecturer(**data)

    # Create students
    for data in student_data:
        User.objects.create_student(**data)

if __name__ == "__main__":
    create_users()
