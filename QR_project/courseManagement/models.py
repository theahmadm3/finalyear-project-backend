from django.db import models
from authentication.models import CustomUser
from django.db.models.constraints import CheckConstraint, Q

class Course(models.Model):
    title = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    lecturer = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to=Q(is_student=False)
    )