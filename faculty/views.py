from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import TeacherWithUserForm  # Use the correct form
from faculty.models import Teacher
from django.contrib.auth.decorators import login_required
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
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, 'faculty/teacher_dashboard.html', {'teacher': teacher})