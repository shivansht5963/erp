from django.db import models
from accounts.models import CustomUser

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    def display_department(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"
    
    def display_courses(self):
        return self.name

class Class(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=10)
    semester = models.IntegerField()
    
    def __str__(self):
        return f"{self.department.name} - Section {self.section} - Semester {self.semester}"
    
    def display_classes(self):
        return f"Section {self.section} - Semester {self.semester}"
    
    def display_student_per_class(self):
        from students.models import Student
        return Student.objects.filter(course__department=self.department, semester=self.semester).count()
    
    def display_courses_per_class(self):
        return Course.objects.filter(department=self.department).count()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    join_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name}"
    
    def mark_attendance(self):
        """Method for marking attendance"""
        pass
    
    def prepare_report_card(self):
        """Method for preparing report cards"""
        pass
    
    def declare_result(self):
        """Method for declaring results"""
        pass
