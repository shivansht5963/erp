# students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from attendance.models import AttendanceReport
from accounts.forms import CustomUserCreationForm
from .forms import StudentForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        # Redirect non-student users to a relevant page or show an error
        return redirect('accounts:login')

    try:
        student = Student.objects.get(user=request.user)
        attendance_reports = AttendanceReport.objects.filter(student=student)

        # Prepare data for the attendance summary chart
        chart_labels = []
        chart_data = []
        if attendance_reports.exists():
            for report in attendance_reports:
                chart_labels.append(report.subject.name)
                chart_data.append(report.attendance_percentage)

        context = {
            'student': student,
            'attendance_reports': attendance_reports,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
        }
        return render(request, 'students/dashboard.html', context)
    except Student.DoesNotExist:
        # Handle cases where a student profile might not exist for a user
        return render(request, 'students/dashboard.html', {'error': 'Student profile not found.'})


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