from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
import math

from .models import Student
from .forms import StudentForm
from accounts.forms import CustomUserCreationForm
from attendance.models import AttendanceReport

User = get_user_model()

def is_student(user):
    """Checks if the authenticated user has the 'student' role."""
    return user.is_authenticated and user.role == 'student'

@user_passes_test(is_student, login_url='accounts:login')
def student_dashboard(request):
    """
    The main backend view for the student dashboard. It securely fetches all
    necessary information for the logged-in student.
    """
    try:
        student = Student.objects.select_related('user', 'course__department').get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Your student profile could not be found. Please contact an administrator.")
        return redirect('accounts:logout')

    # --- Feature: Attendance Data ---
    # Fetch all attendance summary reports for this student.
    # The `view_attendance()` method in the Student model is a convenient shortcut.
    # `select_related('subject')` improves performance by fetching subject details
    # in the same database query.
    attendance_reports = student.view_attendance().select_related('subject')
    
    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        # Placeholders for future features will go here
    }

    return render(request, 'students/student_dashboard.html', context)

# Admin-facing view to add a new student
def add_student(request):
    # This view should be protected, e.g., @user_passes_test(lambda u: u.is_staff)
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student added successfully.")
            return redirect('students:add_student')
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()
        
    return render(request, 'students/add_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })