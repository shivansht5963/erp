# faculty/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TeacherRegistrationForm, DepartmentForm, CourseForm, ClassForm, TeacherForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Updated imports to include the Marks model
from .models import Subject
from students.models import Student
from attendance.models import Attendance
from exams.models import Marks

# --- Existing views (register_teacher, add_department, etc.) ---
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

# --- Dashboard View ---
@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "You are not authorized to view this page.")
        return redirect('accounts:login')

    teacher = request.user.teacher
    subjects_taught = Subject.objects.filter(teacher=teacher)
    
    context = {
        'teacher': teacher,
        'subjects_taught': subjects_taught,
    }
    return render(request, 'faculty/teacher_dashboard.html', context)

# --- Class Detail View (fetches data for all tabs) ---
@login_required
def class_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user.teacher)
    students = Student.objects.filter(course=subject.course, semester=subject.semester).order_by('user__first_name')
    today = timezone.now().date()

    todays_attendance = Attendance.objects.filter(subject=subject, date=today).values_list('student_id', 'status')
    attendance_status = {student_id: status for student_id, status in todays_attendance}

    existing_marks = Marks.objects.filter(subject=subject, student__in=students)
    marks_map = {mark.student_id: mark for mark in existing_marks}

    for student in students:
        student.status = attendance_status.get(student.id, False)
        student.marks_instance = marks_map.get(student.id)

    context = {
        'subject': subject,
        'students': students,
        'today': today,
    }
    return render(request, 'faculty/class_detail.html', context)

# --- View for handling Attendance Form Submission ---
@login_required
def mark_attendance_for_class(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user.teacher)
    
    if request.method == 'POST':
        attendance_date_str = request.POST.get('attendance_date')
        attendance_date = timezone.datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
        students = Student.objects.filter(course=subject.course, semester=subject.semester)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}') == 'on'
            Attendance.objects.update_or_create(
                student=student, subject=subject, date=attendance_date,
                defaults={'status': status, 'marked_by': request.user.teacher}
            )
            
        messages.success(request, f"Attendance for {subject.name} on {attendance_date_str} has been saved.")
        return redirect('faculty:class_detail', subject_id=subject.id)
    return redirect('faculty:class_detail', subject_id=subject.id)


# --- View for handling Marks Form Submission ---
@login_required
def save_marks_for_class(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user.teacher)
    
    if request.method == 'POST':
        students = Student.objects.filter(course=subject.course, semester=subject.semester)
        error_found = False
        for student in students:
            internal_str = request.POST.get(f'internal_marks_{student.id}')
            semester_str = request.POST.get(f'semester_marks_{student.id}')

            # Only process if both fields have some input
            if internal_str and semester_str:
                try:
                    # Try to convert input to numbers
                    internal_marks = float(internal_str)
                    semester_marks = float(semester_str)

                    # Update or create the marks record
                    Marks.objects.update_or_create(
                        student=student,
                        subject=subject,
                        defaults={
                            'internal_marks': internal_marks,
                            'semester_marks': semester_marks
                        }
                    )
                except ValueError:
                    # If conversion fails, it's not a valid number
                    messages.warning(request, f"Invalid mark entered for {student.user.get_full_name()}. Please enter numbers only.")
                    error_found = True
                    continue # Skip to the next student
        
        if not error_found:
            messages.success(request, f"Marks for {subject.name} have been saved successfully.")
        
        return redirect('faculty:class_detail', subject_id=subject.id)
    
    return redirect('faculty:class_detail', subject_id=subject.id)