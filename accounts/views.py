# File: accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from students.models import Student
from faculty.models import Teacher
# We need to import the AttendanceReport model to use it
from attendance.models import AttendanceReport

# Unchanged and correct
@login_required
def redirect_after_login(request):
    if request.user.is_staff:
        return redirect('admin:index')
    elif request.user.role == 'faculty':
        return redirect('accounts:faculty_dashboard')
    elif request.user.role == 'student':
        return redirect('accounts:student_dashboard')
    else:
        return redirect('home')

# Unchanged
@login_required
def faculty_dashboard(request):
    try:
        profile = request.user.teacher
        context = {'teacher': profile}
        return render(request, 'faculty/faculty_dashboard.html', context)
    except Teacher.DoesNotExist:
        context = {'error_message': 'Could not find a faculty profile associated with your account. Please contact an administrator.'}
        return render(request, 'faculty/faculty_dashboard.html', context)

# --- UPDATED STUDENT DASHBOARD VIEW ---
@login_required
def student_dashboard(request):
    try:
        # Get the student profile
        student_profile = request.user.student
        
        # Get the attendance reports for that student
        # The view_attendance() method on your Student model is perfect for this
        attendance_reports = student_profile.view_attendance()

        # Prepare data for the Chart.js pie chart
        chart_labels = [report.subject.name for report in attendance_reports]
        chart_data = [report.attendance_percentage for report in attendance_reports]

        context = {
            'student': student_profile,
            'attendance_reports': attendance_reports,
            'chart_labels': chart_labels,
            'chart_data': chart_data,
        }
        return render(request, 'students/student_dashboard.html', context)

    except Student.DoesNotExist:
        context = {'error_message': 'Could not find a student profile associated with your account. Please contact an administrator.'}
        return render(request, 'students/student_dashboard.html', context)

# Unchanged
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})