# models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
from django.db import models

class StudentManager(BaseUserManager):
    def create_user(self, student_id, password=None, username=None, first_name=None, last_name=None):
        if not student_id:
            raise ValueError('Students must have a student ID')

        user = self.model(
            student_id=student_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, username=None, first_name=None, last_name=None):
        user = self.create_user(
            student_id=student_id,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Student(AbstractBaseUser, PermissionsMixin):
    student_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True, related_name='student_groups')  # Specify related_name
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='student_permissions')  # Specify related_name


    objects = StudentManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.student_id

class LecturerManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('Lecturers must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, first_name=None, last_name=None):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Lecturer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(Group, blank=True, related_name='lecturer_groups') 
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='lecturer_permissions') # Specify related_name

    objects = LecturerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
