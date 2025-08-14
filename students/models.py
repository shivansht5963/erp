from django.db import models
from django.conf import settings
from faculty.models import Course, Class
import math

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField()
    dob = models.DateField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.roll_number} - {self.user.first_name} {self.user.last_name}"
    
    def get_current_year(self):
        """Calculates the academic year based on the semester."""
        if self.semester and self.semester > 0:
            # Semesters 1,2 -> Year 1
            # Semesters 3,4 -> Year 2
            # etc.
            return math.ceil(self.semester / 2)
        return "N/A"
    
    def view_attendance(self):
        """Method to view student's attendance"""
        from attendance.models import AttendanceReport
        return AttendanceReport.objects.filter(student=self)
    
    def view_marks(self):
        """Method to view student's marks"""
        from exams.models import Marks
        return Marks.objects.filter(student=self)
    
    def communicate_with_teacher(self):
        """Method for student-teacher communication"""
        pass
    
    def communicate_with_other_student(self):
        """Method for student-student communication"""
        pass

class StudentInfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attended_classes = models.IntegerField(default=0)
    total_classes = models.IntegerField(default=0)
    attendance_percentage = models.FloatField(default=0.0)
    marks = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.course.name}"
    
    def display_attendance(self):
        """Method to display attendance"""
        if self.total_classes > 0:
            return f"{self.attendance_percentage:.2f}%"
        return "0.00%"
    
    def display_marks(self):
        """Method to display marks"""
        return f"{self.marks:.2f}"
    
    def save(self, *args, **kwargs):
        if self.total_classes > 0:
            self.attendance_percentage = (self.attended_classes / self.total_classes) * 100
        super().save(*args, **kwargs)
