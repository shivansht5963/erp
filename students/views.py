# students/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentForm
from accounts.forms import CustomUserCreationForm
from attendance.models import AttendanceReport
from exams.models import Marks
from fees.models import FeePayment
from .models import Student
import json

def add_student(request):
    """
    Handles the creation of a new student and their associated user account.
    """
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.save()
            
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            
            messages.success(request, "Student added successfully.")
            return redirect('students:add_student')
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()
        
    return render(request, 'students/add_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, "No student profile is associated with your account.")
        return redirect('accounts:login')

    student = request.user.student
    
    attendance_reports = AttendanceReport.objects.filter(student=student)
    marks_reports = Marks.objects.filter(student=student)
    fee_payment = FeePayment.objects.filter(student=student).order_by('-fee_structure__due_date').first()

    if fee_payment and fee_payment.fee_structure:
        total_fee = fee_payment.fee_structure.amount
        amount_paid = fee_payment.amount_paid
        amount_due = total_fee - amount_paid
    else:
        total_fee, amount_paid, amount_due = 0, 0, 0
    
    # Prepare data for the donut chart
    chart_labels = []
    chart_data = []
    for report in attendance_reports:
        chart_labels.append(report.subject.name)
        chart_data.append(report.attendance_percentage)
        
    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'marks_reports': marks_reports,
        'fee_payment': fee_payment,
        'total_fee': total_fee,
        'amount_paid': amount_paid,
        'amount_due': amount_due,
        # Pass chart data to the template, safely converted to JSON
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'students/student_dashboard.html', context)