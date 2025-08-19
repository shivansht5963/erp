# File: erp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    """
    This view now correctly renders your main landing page.
    """
    return render(request, 'index.html')

@login_required
def dashboard_redirect(request):
    """
    This view is now ONLY used after a successful login to redirect
    users to their appropriate dashboard based on their role.
    """
    if request.user.role == 'student':
        return redirect('students:student_dashboard')
    
    elif request.user.role == 'faculty':
        return redirect('admin:index')

    elif request.user.role == 'admin':
        return redirect('admin:index')
        
    else:
        return redirect('accounts:login')