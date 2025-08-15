
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SubjectForm, MarksForm
from faculty.models import Teacher, Subject
from students.models import Student
from .models import Marks
from django.contrib import messages

@login_required
def update_marks(request, pk):
    # Only allow teachers
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Only teachers can update marks.")
        return redirect('accounts:login')
    teacher = request.user.teacher
    mark = get_object_or_404(Marks, pk=pk)
    # Only allow update if teacher teaches this subject
    if mark.subject.teacher != teacher:
        messages.error(request, "You are not allowed to update marks for this subject.")
        return redirect('exams:add_marks')
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        form.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)
        form.fields['student'].queryset = Student.objects.filter(course=mark.subject.course, semester=mark.subject.semester)
        if form.is_valid():
            form.save()
            messages.success(request, "Marks updated successfully.")
            return redirect('exams:add_marks')
    else:
        form = MarksForm(instance=mark)
        form.fields['subject'].queryset = Subject.objects.filter(teacher=teacher)
        form.fields['student'].queryset = Student.objects.filter(course=mark.subject.course, semester=mark.subject.semester)
    return render(request, 'exams/update_marks.html', {'form': form, 'mark': mark})

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams:add_subject')
    else:
        form = SubjectForm()
    return render(request, 'exams/add_subject.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SubjectForm, MarksForm
from faculty.models import Teacher, Subject
from students.models import Student
from .models import Marks
from django.contrib import messages

@login_required
def add_marks(request):
    # Only allow teachers
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Only teachers can add marks.")
        return redirect('accounts:login')
    teacher = request.user.teacher
    # Only show subjects taught by this teacher
    subjects = Subject.objects.filter(teacher=teacher)
    # Only show students in the teacher's subjects' courses and semesters
    students = Student.objects.filter(course__in=subjects.values_list('course', flat=True), semester__in=subjects.values_list('semester', flat=True))
    if request.method == 'POST':
        form = MarksForm(request.POST)
        form.fields['subject'].queryset = subjects
        form.fields['student'].queryset = students
        if form.is_valid():
            form.save()
            messages.success(request, "Marks added successfully.")
            return redirect('exams:add_marks')
    else:
        form = MarksForm()
        form.fields['subject'].queryset = subjects
        form.fields['student'].queryset = students
    # Show marks already entered by this teacher for their subjects
    marks = Marks.objects.filter(subject__in=subjects)
    return render(request, 'exams/add_marks.html', {'form': form, 'marks': marks})
