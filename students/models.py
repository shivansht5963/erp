from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.roll_number} - {self.user.first_name} {self.user.last_name}"
