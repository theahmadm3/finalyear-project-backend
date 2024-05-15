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


    class Meta:
        # Define a unique constraint to ensure that a student can only take one course
        unique_together = ('student', 'course_details')

    def __str__(self):
        return f"{self.student}'s Course: {self.course_details}"





# Create your models here.
