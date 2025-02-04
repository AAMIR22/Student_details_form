from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PhoneNumber(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    school = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    comments = models.CharField(max_length=500)
    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student_name} - {self.number}"

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    password_backup = models.CharField(max_length=100)