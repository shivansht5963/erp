from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from notifications.models import Notification
from students.models import Student
import json

# This view for adding a user remains unchanged.
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})


# --- THIS IS THE CORRECTED AND COMPLETED STUDENT DASHBOARD VIEW ---
@login_required
def student_dashboard(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return redirect('home') 

    # Fetch all necessary data
    student_notifications = Notification.objects.filter(recipient=student).order_by('-created_at')[:5]
    attendance_reports = student.view_attendance()

    # --- NEW: Prepare data specifically for the Chart.js pie chart ---
    chart_labels = [report.subject.name for report in attendance_reports]
    chart_data = [report.attendance_percentage for report in attendance_reports]

    # Pass all the data into the template context.
    context = {
        'student': student,
        'notifications': student_notifications,
        'attendance_reports': attendance_reports,
        # We use json.dumps to safely pass the lists to the template's JavaScript
        'chart_labels_json': json.dumps(chart_labels),
        'chart_data_json': json.dumps(chart_data),
    }
    
    return render(request, 'students/student_dashboard.html', context)

@login_required
def dashboard(request):
    """
    Redirects users to their appropriate dashboard based on their role.
    """
    user = request.user
    
    if user.role == 'student':
        # If the user's role is 'student', send them to the student dashboard.
        return redirect('accounts:student_dashboard')
        
    elif user.role == 'faculty':
        # For now, faculty and admins will be sent to the main admin site.
        # Later, you can create a dedicated faculty dashboard.
        return redirect('admin:index')
        
    elif user.is_superuser or user.role == 'admin':
        # Superusers and admins also go to the main admin site.
        return redirect('admin:index')
        
    else:
        # As a fallback, send any other users to the homepage.
        return redirect('home')