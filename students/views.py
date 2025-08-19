# File: students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from .forms import StudentForm
from .models import Student
from attendance.models import AttendanceReport
from accounts.models import Notification  # Import your Notification model
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@login_required
def student_dashboard(request):
    """
    Displays the dashboard for the logged-in student.
    """
    if request.user.role != 'student':
        # Redirect non-students away
        return redirect('accounts:login') 

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # This is a fallback in case a user with role 'student' doesn't have a student profile.
        return render(request, 'error.html', {'message': 'Student profile not found.'})

    # Fetch attendance reports for the student
    attendance_reports = AttendanceReport.objects.filter(student=student)
    
    # --- START OF THE FIX ---
    # Fetch the 5 most recent notifications sent ONLY to the currently logged-in user.
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    # --- END OF THE FIX ---

    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'notifications': recent_notifications,
    }
    return render(request, 'students/student_dashboard.html', context)


# This is your existing function, it remains the same.
# @user_passes_test(lambda u: u.is_staff)
def add_student(request):
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