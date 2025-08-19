# File: students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from .forms import StudentForm
from .models import Student
from attendance.models import AttendanceReport
from accounts.models import Notification
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q  # <--- THIS IS THE MISSING LINE TO FIX THE ERROR

User = get_user_model()

@login_required
def student_dashboard(request):
    """
    Displays the dashboard for the logged-in student.
    """
    if request.user.role != 'student':
        return redirect('accounts:login') 

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found.'})

    attendance_reports = AttendanceReport.objects.filter(student=student)
    
    # This query now works because 'Q' is imported.
    # It fetches notifications sent to the specific student OR to all students.
    recent_notifications = Notification.objects.filter(
        Q(recipient=request.user) | Q(send_to_all_students=True)
    ).distinct().order_by('-created_at')[:5]

    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'notifications': recent_notifications,
    }
    return render(request, 'students/student_dashboard.html', context)


# This is your existing function, it remains the same.
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