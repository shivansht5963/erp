from django.db import models
from students.models import Student
from faculty.models import Subject

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    internal_marks = models.FloatField()
    semester_marks = models.FloatField()
    total_marks = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.semester_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code}"
