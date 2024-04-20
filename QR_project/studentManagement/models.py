from django.db import models
from authentication.models import CustomUser
from courseManagement.models import Course
from django.db.models.constraints import CheckConstraint, Q
class StudentCourses(models.Model):
    course_details=models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    student = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_student=True)
    )





# Create your models here.
