from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherWithUserForm  # Use the correct form

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherWithUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! You can now log in.")
            return redirect('accounts:login')  # Use correct login URL name
    else:
        form = TeacherWithUserForm()
    return render(request, 'faculty/register_teacher.html', {'form': form})

def teacher_dashboard(request):
    return render(request, 'faculty/teacher_dashboard.html')