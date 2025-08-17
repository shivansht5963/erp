# File: erp/context_processors.py

from students.models import Student
from faculty.models import Teacher
from django.contrib import messages

def user_profile_processor(request):
    """
    Adds user-specific profile information to the context for every template.
    It checks the user's role and fetches the correct profile (Student or Teacher).
    """
    context = {}
    if request.user.is_authenticated:
        # Check if the logged-in user has a 'role' attribute
        if hasattr(request.user, 'role'):

            # If the user is a student, try to get their student profile
            if request.user.role == 'student':
                try:
                    context['student_profile'] = request.user.student
                except Student.DoesNotExist:
                    # This message will now ONLY show for students with missing profiles
                    messages.error(request, 'Your student profile could not be found. Please contact an administrator.')

            # If the user is faculty, try to get their teacher profile
            elif request.user.role == 'faculty':
                try:
                    context['teacher_profile'] = request.user.teacher
                except Teacher.DoesNotExist:
                    messages.error(request, 'Your faculty profile could not be found. Please contact an administrator.')
    
    return context