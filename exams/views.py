from django.shortcuts import render, redirect
from .forms import SubjectForm, MarksForm

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams:add_subject')
    else:
        form = SubjectForm()
    return render(request, 'exams/add_subject.html', {'form': form})

def add_marks(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exams:add_marks')
    else:
        form = MarksForm()
    return render(request, 'exams/add_marks.html', {'form': form})
