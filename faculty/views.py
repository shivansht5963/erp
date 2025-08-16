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
def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! You can now log in.")
            return redirect('accounts:login')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'faculty/register_teacher.html', {'form': form})

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:add_department')
    else:
        form = DepartmentForm()
    return render(request, 'faculty/add_department.html', {'form': form})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:add_course')
    else:
        form = CourseForm()
    return render(request, 'faculty/add_course.html', {'form': form})

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:add_class')
    else:
        form = ClassForm()
    return render(request, 'faculty/add_class.html', {'form': form})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:add_teacher')
    else:
        form = TeacherForm()
    return render(request, 'faculty/add_teacher.html', {'form': form})