

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from students.models import Student
from attendance.models import AttendanceReport
from notifications.models import Notification  # Import your existing Notification model

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

    # Fetch attendance reports for the student
    attendance_reports = AttendanceReport.objects.filter(student=student)
    
    # Fetch the 5 most recent notifications
    # Note: I am assuming your model is named 'Notification'
    recent_notifications = Notification.objects.all().order_by('-created_at')[:5]

    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'notifications': recent_notifications, # Pass notifications to the template
    }
    return render(request, 'accounts/student_dashboard.html', context)


def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})