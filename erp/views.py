# erp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')


@login_required
def role_based_redirect(request):
    """
    Redirects users to their respective dashboards based on their role after login.
    """
    if request.user.role == 'faculty':
        return redirect('faculty:teacher_dashboard')
        
    elif request.user.role == 'student':
        # THIS IS THE CORRECTED REDIRECT FOR STUDENTS
        return redirect('students:student_dashboard')
        
    else:
        # Admins and any other roles will go to the admin panel by default.
        return redirect('admin:index')