from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeacherRegistrationForm, DepartmentForm, CourseForm, ClassForm, TeacherForm
from .models import Teacher, Subject
from students.models import Student  # Added for mark_attendance
from attendance.models import Attendance # Added for mark_attendance

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

@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        subjects = Subject.objects.filter(teacher=teacher)
        context = {
            'teacher': teacher,
            'subjects': subjects
        }
        return render(request, 'faculty/teacher_dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('accounts:login')

# --- THIS IS THE SECOND MISSING FUNCTION THAT HAS BEEN ADDED BACK ---
@login_required
def mark_attendance(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # Assuming students are enrolled in the course that the subject belongs to
    students = Student.objects.filter(course=subject.course)
    
    if request.method == 'POST':
        # Logic to process the submitted attendance data
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                # Create or update attendance record
                Attendance.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=request.POST.get('attendance_date'),
                    defaults={'status': status == 'present'}
                )
        messages.success(request, f"Attendance marked for {subject.name}.")
        return redirect('faculty:teacher_dashboard')

    context = {
        'subject': subject,
        'students': students
    }
    return render(request, 'faculty/mark_attendance.html', context)