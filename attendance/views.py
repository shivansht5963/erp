from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .forms import AttendanceForm, AttendanceReportForm
from faculty.models import Subject
from students.models import Student
from .models import Attendance
from accounts.decorators import is_faculty

@login_required
@user_passes_test(is_faculty, login_url='/accounts/login/')
def mark_attendance_for_subject(request, subject_id):
    """
    View for a teacher to mark attendance for all students
    in a class associated with a specific subject.
    """
    subject = get_object_or_404(Subject, id=subject_id)
    if subject.teacher != request.user.teacher:
        messages.error(request, "You are not authorized to mark attendance for this subject.")
        return redirect('faculty:teacher_dashboard')

    students = Student.objects.filter(
        course__department__in=subject.teacher.departments.all(),
        semester=subject.semester
    ).order_by('roll_number')

    if request.method == 'POST':
        present_student_ids = request.POST.getlist('present_students')
        
        # --- THIS IS THE FIX ---
        # Define 'today' once, before the loop.
        today = timezone.now().date()

        for student in students:
            is_present = str(student.id) in present_student_ids
            
            attendance_record, created = Attendance.objects.get_or_create(
                student=student,
                subject=subject,
                date=today,
                defaults={'status': is_present, 'marked_by': request.user.teacher}
            )
            
            if not created:
                attendance_record.status = is_present
                attendance_record.save()
        
        # Now the 'today' variable is accessible here.
        messages.success(request, f"Attendance for {subject.name} on {today} has been saved successfully.")
        return redirect('faculty:teacher_dashboard')

    context = {
        'subject': subject,
        'students': students
    }
    return render(request, 'attendance/mark_attendance_form.html', context)


# --- Keep your other views below ---

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:add_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/add_attendance.html', {'form': form})

def add_attendance_report(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:add_attendance_report')
    else:
        form = AttendanceReportForm()
    return render(request, 'attendance/add_attendance_report.html', {'form': form})