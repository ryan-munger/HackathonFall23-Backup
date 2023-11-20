from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    GRADE_CHOICES = (
        ("college", "College"),
        ("highschool", "High School"),
        ("middle_school", "Middle School"),
    )
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)