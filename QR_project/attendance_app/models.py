from django.db import models
from authentication.models import CustomUser as User
from courseManagement.models import Course
from django.utils import timezone

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    time_frame = models.CharField(max_length=100,default=True)
    lecturer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_student':False}
    )




    
class LecturerAttendance(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, 
                                 on_delete=models.CASCADE,
                                 limit_choices_to={'is_student':False},
                                 null=True,blank=True)
    timestamp = models.DateTimeField()
    def save(self, *args, **kwargs):
        # Convert timestamp to local time
        self.timestamp = timezone.localtime(self.timestamp)
        super().save(*args, **kwargs)

class StudentAttendance(models.Model):
    lecture_attendance= models.ForeignKey(LecturerAttendance, on_delete=models.CASCADE,default=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    #location = models.CharField(max_length=100)

   

