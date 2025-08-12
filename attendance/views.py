from django.shortcuts import render, redirect
from .forms import AttendanceForm, AttendanceReportForm

def add_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:add_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/add_attendance.html', {'form': form})

def add_attendance_report(request):
    if request.method == 'POST':
        form = AttendanceReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance:add_attendance_report')
    else:
        form = AttendanceReportForm()
    return render(request, 'attendance/add_attendance_report.html', {'form': form})
