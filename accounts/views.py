from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from notifications.models import Notification
from students.models import Student
import json

# This view for adding a user remains unchanged.
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})


@login_required
def dashboard(request):
    """
    Redirects users to their appropriate dashboard based on their role.
    """
    user = request.user
    
    if user.role == 'student':
        # If the user's role is 'student', send them to the student dashboard.
        return redirect('students:dashboard')
        
    elif user.role == 'faculty':
        # For now, faculty and admins will be sent to the main admin site.
        # Later, you can create a dedicated faculty dashboard.
        return redirect('admin:index')
        
    elif user.is_superuser or user.role == 'admin':
        # Superusers and admins also go to the main admin site.
        return redirect('admin:index')
        
    else:
        # As a fallback, send any other users to the homepage.
        return redirect('home')