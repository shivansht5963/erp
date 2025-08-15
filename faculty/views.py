from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TeacherRegistrationForm, DepartmentForm, CourseForm, ClassForm, TeacherForm

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

def teacher_dashboard(request):
    return render(request, 'faculty/teacher_dashboard.html')