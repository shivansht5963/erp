<<<<<<< HEAD
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import TeacherWithUserForm  # Use the correct form
from faculty.models import Teacher
from django.contrib.auth.decorators import login_required
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.dateparse import parse_date
from django.db import transaction

from .forms import TeacherRegistrationForm, DepartmentForm, CourseForm, ClassForm, TeacherForm
from .models import Teacher, Subject
from students.models import Student
from attendance.models import Attendance

# Helper function for role checking
def is_teacher(user):
    return user.is_authenticated and user.role == 'faculty'

# Teacher Dashboard View
@user_passes_test(is_teacher, login_url='accounts:login')
def teacher_dashboard(request):
    try:
        # Assumes a related_name of 'teacher' is on the user model, or gets it this way
        teacher = Teacher.objects.get(user=request.user)
        subjects = Subject.objects.filter(teacher=teacher)
        context = {
            'teacher': teacher,
            'subjects': subjects,
        }
        return render(request, 'faculty/teacher_dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "Your teacher profile is not set up.")
        return redirect('accounts:logout')

# Mark Attendance View
@user_passes_test(is_teacher, login_url='accounts:login')
def mark_attendance(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher__user=request.user) # Security check
    students = Student.objects.filter(course=subject.course, semester=subject.semester).order_by('roll_number')

    if request.method == 'POST':
        attendance_date_str = request.POST.get('attendance_date')
        attendance_date = parse_date(attendance_date_str)
        present_student_ids = request.POST.getlist('present_students')

        if not attendance_date:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return redirect('faculty:mark_attendance', subject_id=subject.id)

        try:
            with transaction.atomic():
                for student in students:
                    status = str(student.id) in present_student_ids
                    
                    Attendance.objects.update_or_create(
                        student=student,
                        subject=subject,
                        date=attendance_date,
                        defaults={'status': status, 'marked_by': request.user.teacher}
                    )
            messages.success(request, f"Attendance for {attendance_date_str} saved successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            
        return redirect('faculty:mark_attendance', subject_id=subject.id)
    
    context = {
        'subject': subject,
        'students': students,
    }
    return render(request, 'faculty/mark_attendance.html', context)

# Existing Admin-facing views
>>>>>>> 2b80914a11edc1d0606b968936c459262e2b7817
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! You can now log in.")
            return redirect('accounts:login')
    else:
        form = TeacherWithUserForm()
    return render(request, 'faculty/register_teacher.html', {'form': form})
@login_required
def teacher_dashboard(request):
<<<<<<< HEAD
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, 'faculty/teacher_dashboard.html', {'teacher': teacher})
=======
    return render(request, 'faculty/teacher_dashboard.html')
>>>>>>> 2b80914a11edc1d0606b968936c459262e2b7817
