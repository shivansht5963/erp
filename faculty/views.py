from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherRegistrationForm

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher registered successfully! You can now log in.")
            return redirect('login')  # login page from accounts app
    else:
        form = TeacherRegistrationForm()
    return render(request, 'faculty/register_teacher.html', {'form': form})
