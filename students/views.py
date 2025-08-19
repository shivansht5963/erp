

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum

from accounts.forms import CustomUserCreationForm
from .forms import StudentForm
from .models import Student
from attendance.models import AttendanceReport
from faculty.models import Announcement, Class

User = get_user_model()


def add_student(request):
    """
    Handles the creation of a new student user and their associated student profile.
    """
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
        
    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'students/add_student.html', context)


@login_required
def student_dashboard(request):
    """
    Gathers all necessary data and displays the main dashboard for a logged-in student.
    """
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, 'students/no_profile.html')

    attendance_reports = AttendanceReport.objects.filter(student=student).order_by('subject__name')

    overall_summary = attendance_reports.aggregate(
        total_attended=Sum('classes_attended'),
        total_possible=Sum('total_classes')
    )
    total_attended = overall_summary.get('total_attended') or 0
    total_possible = overall_summary.get('total_possible') or 0
    
    if total_possible > 0:
        overall_attendance_percentage = round((total_attended / total_possible) * 100, 2)
    else:
        overall_attendance_percentage = 0.0

    # --- CORRECTED ANNOUNCEMENT LOGIC ---
    # Uses the student's direct class assignment for accurate filtering.
    if student.class_assigned:
        recent_announcements = Announcement.objects.filter(
            Q(target_class=student.class_assigned) | Q(target_class__isnull=True)
        ).order_by('-created_at')[:5]
    else:
        # If student has no class assigned, show only global announcements.
        recent_announcements = Announcement.objects.filter(target_class__isnull=True).order_by('-created_at')[:5]
        print(f"DEBUG for {student.user.username}: Attended={overall_attendance_percentage}%, Absent={100 - overall_attendance_percentage}%")

    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'recent_announcements': recent_announcements,
        'chart_data': {
            'attended': overall_attendance_percentage,
            'absent': 100 - overall_attendance_percentage,
        }
    }
    
    return render(request, 'students/dashboard.html', context)