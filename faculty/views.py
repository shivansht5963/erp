from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TeacherRegistrationForm, DepartmentForm, CourseForm, ClassForm, TeacherForm

# Import necessary forms and models
from notifications.forms import TeacherNotificationForm
from notifications.models import Notification
from students.models import Student
from accounts.models import CustomUser
from accounts.decorators import is_faculty

# --- THIS IS THE FIX ---
# Import the Teacher and Subject models from the same app's models.py file
from .models import Teacher, Subject
@user_passes_test(is_faculty)
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "Your teacher profile could not be found. Please contact an administrator.")
        return redirect('accounts:logout')

    if request.method == 'POST':
        # --- PASS 'teacher' OBJECT TO THE FORM ON POST ---
        form = TeacherNotificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            notification = Notification.objects.create(
                title=data['title'],
                message=data['message'],
                created_by=request.user
            )
            # Logic for faculty is to send to a specific class
            target_class = data['target_class']
            students_in_class = Student.objects.filter(
                course__department=target_class.department, 
                semester=target_class.semester
            )
            recipients = [student.user for student in students_in_class]
            for user in recipients:
                Notification.objects.create(user=user, notification=notification)
            messages.success(request, f'Notification sent to class {target_class} successfully!')
            return redirect('faculty:teacher_dashboard')
    
    else:
        # --- PASS 'teacher' OBJECT TO THE FORM ON GET ---
       form = TeacherNotificationForm(request.POST)

    subjects = Subject.objects.filter(teacher=teacher)
    sent_notifications = Notification.objects.filter(created_by=request.user).order_by('-created_at')[:5]

    context = {
        'teacher': teacher,
        'form': form,
        'sent_notifications': sent_notifications,
        'subjects': subjects,
    }
    return render(request, 'faculty/dashboard_teacher.html', context)


# --- Keep all your existing views below ---

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! You can now log in.")
            return redirect('accounts:login')  # Use the name of the login URL
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