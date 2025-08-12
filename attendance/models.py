from django.db import models
from students.models import Student
from faculty.models import Subject
from faculty.models import Teacher

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(default=False)  # True for present, False for absent
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'date']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.date}"

class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_classes = models.IntegerField(default=0)
    classes_attended = models.IntegerField(default=0)
    attendance_percentage = models.FloatField(default=0.0)
    
    class Meta:
        unique_together = ['student', 'subject']
    
    def calculate_attendance(self):
        if self.total_classes > 0:
            self.attendance_percentage = (self.classes_attended / self.total_classes) * 100
        else:
            self.attendance_percentage = 0
    
    def save(self, *args, **kwargs):
        self.calculate_attendance()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.attendance_percentage:.2f}%"