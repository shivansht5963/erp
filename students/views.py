from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from attendance.models import AttendanceReport

# App-specific Imports
from .models import Student
from .forms import StudentForm
from accounts.forms import CustomUserCreationForm


User = get_user_model()

def is_student(user):
    """
    A helper function for the @user_passes_test decorator.
    It checks if the logged-in user has the 'student' role.
    This is a clean and reusable way to handle role-based authorization.
    """
    return user.is_authenticated and user.role == 'student'

@user_passes_test(is_student, login_url='accounts:login')
def student_dashboard(request):
    """
    This is the main backend view for the student dashboard.
    It's the central hub for all student-related information.

    Backend Logic:
    1.  **Authorization:** Uses @user_passes_test to ensure only authenticated
        users with the 'student' role can access this view.
    2.  **Security:** Fetches the Student profile that is directly linked to the
        logged-in user (`request.user`). This prevents any possibility of one
        student viewing another's data.
    3.  **Error Handling:** Includes a try-except block to gracefully handle the
        edge case where a 'student' user might not have a corresponding Student
        profile, preventing a server crash.
    4.  **Performance:** Uses `select_related` to fetch the student's related
        user, course, and department data in a single, efficient database query,
        avoiding the "N+1 query problem".
    """
    try:
        # Fetch the single Student object that matches the currently logged-in user.
        student = Student.objects.select_related(
            'user',
            'course__department'  # Follows the foreign key to Course, then to Department
        ).get(user=request.user)

    except Student.DoesNotExist:
        # This is a critical safety net. If a user is marked as a student but
        # has no profile, log them out and show an error.
        messages.error(request, "Your student profile could not be found. Please contact an administrator.")
        return redirect('accounts:logout')

    # --- Data for "Feature 1: Student Details" ---
    # The 'student' object itself contains all the necessary details.
    # We will add data for other features to this context dictionary later.
    attendance_reports = student.view_attendance().select_related('subject')
    
    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        
    }

    # Render the frontend template, passing the context dictionary
    # which contains all the data the template needs.
    return render(request, 'students/student_dashboard.html', context)

# @user_passes_test(lambda u: u.is_staff) # It's good practice to protect this view
def add_student(request):
    """
    Handles the creation of a new student record, which involves creating
    a CustomUser and a related Student profile simultaneously.
    """
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)
        
        # Check if both forms contain valid data
        if user_form.is_valid() and student_form.is_valid():
            # First, save the user account
            user = user_form.save(commit=False)
            user.role = 'student'  # Set the role explicitly
            user.save()

            # Now, create the student profile but don't save to DB yet
            student = student_form.save(commit=False)
            # Link the profile to the user account we just created
            student.user = user
            student.save() # Now save the complete student profile to the DB

            messages.success(request, "Student added successfully.")
            return redirect('students:add_student')
    else:
        # If the request is a GET, create new, empty forms
        user_form = CustomUserCreationForm()
        student_form = StudentForm()

    # Pass the forms to the template
    return render(request, 'students/add_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })