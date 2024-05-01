from django.contrib import admin
from .models import Lecture, StudentAttendance, LecturerAttendance

admin.site.register(Lecture)
admin.site.register(StudentAttendance)
admin.site.register(LecturerAttendance)

# Register your models here.
