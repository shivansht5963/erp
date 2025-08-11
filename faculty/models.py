from django.db import models
from accounts.models import CustomUser

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    join_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"
