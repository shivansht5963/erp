# erp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    """
    Renders the main homepage.
    """
    return render(request, 'index.html')

@login_required
def login_redirect(request):
    """
    This view acts as a router after a user logs in.
    It checks the user's role and redirects them to the appropriate dashboard.
    - Superusers and Faculty go to the admin site.
    - Students go to their specific dashboard.
    """
    # Superusers have the highest priority
    if request.user.is_superuser:
        return redirect('admin:index')

    # Check the custom 'role' field on your CustomUser model
    if hasattr(request.user, 'role'):
        if request.user.role == 'student':
            return redirect('students:dashboard')
        
        if request.user.role == 'faculty':
            return redirect('admin:index')

    # As a fallback, redirect any other authenticated user to the admin index.
    # This is a safe default for staff members who might not have a specific role.
    return redirect('admin:index')