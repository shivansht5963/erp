# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import Student
from .forms import CustomUserForm
import json

@login_required
def dashboard(request):
    """Redirects user to the appropriate dashboard based on their role."""
    user = request.user
    if user.role == 'student':
        return redirect('accounts:student_dashboard')
    elif user.role == 'faculty':
        # You can create a faculty_dashboard view and URL similar to the student one
        # For now, we'll redirect them to a placeholder or admin
        return redirect('/admin/') 
    elif user.role == 'admin':
        return redirect('/admin/')
    else:
        # Fallback for any other case
        return redirect('accounts:login')

@login_required
def student_dashboard(request):
    """Displays the dashboard for a logged-in student."""
    try:
        # Get the student profile linked to the logged-in user
        student = request.user.student
    except Student.DoesNotExist:
        # Handle cases where a user with a student role has no student profile
        # You might want to create an error.html template for this
        return render(request, 'accounts/login.html', {'error': 'Student profile not found.'})

    # Fetch detailed attendance reports using the model method
    attendance_reports = student.view_attendance()

    # Prepare data for the pie chart
    chart_labels = [report.subject.name for report in attendance_reports]
    chart_data = [report.attendance_percentage for report in attendance_reports]

    # Combine user and student data into a single context
    context = {
        'student': student,
        'user': request.user, # Pass the user object for general info like name/email
        'attendance_reports': attendance_reports,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'accounts/dashboard_student.html', context)


def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})