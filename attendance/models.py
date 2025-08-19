from django.db import models
from students.models import Student
from faculty.models import Subject, Teacher

class Attendance(models.Model):
    """
    Records a daily attendance entry. Now tracks the number of classes.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()

    classes_held = models.PositiveIntegerField(
        default=1,
        help_text="Total number of classes held on this date."
    )
    classes_attended = models.PositiveIntegerField(
        default=1,
        help_text="Number of classes the student attended on this date."
    )

    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'subject', 'date']
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.date}"


class AttendanceReport(models.Model):
    """
    Summarizes attendance for a student in a subject. This model is unchanged.
    The signals will now update its fields automatically.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_classes = models.IntegerField(default=0)      # This will now store the sum of 'classes_held'
    classes_attended = models.IntegerField(default=0)   # This will now store the sum of 'classes_attended'
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