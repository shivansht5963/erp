from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib import messages
from django.core.paginator import Paginator

from students.models import Student
from .models import FeeCategory, FeeStructure, FeePayment, FeeReminder
from .forms import FeeCategoryForm, FeeStructureForm, FeePaymentForm, FeeReminderForm

# Helper function to get student object for the current user
def get_student_for_user(user):
    try:
        return Student.objects.get(user=user)
    except Student.DoesNotExist:
        return None

def add_fee_category(request):
    if request.method == 'POST':
        form = FeeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fees:add_fee_category')
    else:
        form = FeeCategoryForm()
    return render(request, 'fees/add_fee_category.html', {'form': form})

def add_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fees:add_fee_structure')
    else:
        form = FeeStructureForm()
    return render(request, 'fees/add_fee_structure.html', {'form': form})

def add_fee_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fees:add_fee_payment')
    else:
        form = FeePaymentForm()
    return render(request, 'fees/add_fee_payment.html', {'form': form})

@login_required
def student_fee_dashboard(request):
    """Dashboard for students to view their fee status and reminders"""
    student = get_student_for_user(request.user)
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect('home')  # Or appropriate redirect
    
    # Get all fee payments for the student
    fee_payments = FeePayment.objects.filter(
        student=student
    ).select_related('fee_structure').order_by('-due_date')
    
    # Calculate summary statistics
    total_fees = fee_payments.aggregate(total=Sum('total_amount'))['total'] or 0
    total_paid = fee_payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_due = total_fees - total_paid
    
    # Get upcoming and overdue payments
    today = timezone.now().date()
    upcoming_payments = fee_payments.filter(
        due_date__gte=today,
        payment_status__in=['pending', 'partial']
    ).order_by('due_date')[:5]
    
    overdue_payments = fee_payments.filter(
        due_date__lt=today,
        payment_status__in=['pending', 'partial', 'overdue']
    ).order_by('due_date')[:5]
    
    # Get recent payments
    recent_payments = fee_payments.filter(
        amount_paid__gt=0
    ).order_by('-payment_date')[:5]
    
    # Get active reminders
    active_reminders = FeeReminder.objects.filter(
        fee_payment__student=student,
        sent=False,
        reminder_date__lte=today
    ).select_related('fee_payment__fee_structure').order_by('reminder_date')
    
    context = {
        'student': student,
        'total_fees': total_fees,
        'total_paid': total_paid,
        'total_due': total_due,
        'upcoming_payments': upcoming_payments,
        'overdue_payments': overdue_payments,
        'recent_payments': recent_payments,
        'active_reminders': active_reminders,
    }
    
    return render(request, 'fees/student_dashboard.html', context)

@login_required
def fee_payment_detail(request, payment_id):
    """Detailed view of a specific fee payment"""
    student = get_student_for_user(request.user)
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect('home')
    
    payment = get_object_or_404(
        FeePayment,
        id=payment_id,
        student=student
    )
    
    # Get payment history for this fee structure
    payment_history = FeePayment.objects.filter(
        student=student,
        fee_structure=payment.fee_structure,
        amount_paid__gt=0
    ).order_by('-payment_date')
    
    context = {
        'payment': payment,
        'payment_history': payment_history,
    }
    
    return render(request, 'fees/fee_payment_detail.html', context)

@login_required
def all_fee_payments(request):
    """View all fee payments with filtering and pagination"""
    student = get_student_for_user(request.user)
    if not student:
        messages.error(request, "Student profile not found.")
        return redirect('home')
    
    # Get filter parameters
    status = request.GET.get('status', '')
    year = request.GET.get('year', '')
    
    # Start with base queryset
    payments = FeePayment.objects.filter(
        student=student
    ).select_related('fee_structure').order_by('-due_date')
    
    # Apply filters
    if status:
        payments = payments.filter(payment_status=status)
    if year:
        payments = payments.filter(fee_structure__academic_year=year)
    
    # Get unique academic years for filter dropdown
    academic_years = FeeStructure.objects.values_list('academic_year', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(payments, 10)  # Show 10 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
        'year': year,
        'academic_years': academic_years,
        'status_choices': dict(FeePayment.PAYMENT_STATUS_CHOICES),
    }
    
    return render(request, 'fees/all_fee_payments.html', context)

# Admin views
def add_fee_category(request):
    if request.method == 'POST':
        form = FeeCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee category added successfully.')
            return redirect('fees:add_fee_category')
    else:
        form = FeeCategoryForm()
    return render(request, 'fees/add_fee_category.html', {'form': form})

def add_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            fee_structure = form.save()
            messages.success(request, 'Fee structure added successfully.')
            return redirect('fees:add_fee_structure')
    else:
        form = FeeStructureForm()
    return render(request, 'fees/add_fee_structure.html', {'form': form})

def add_fee_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            # Set the category from the student's category if not set
            if not payment.category and payment.student:
                payment.category = payment.student.category
            payment.save()
            messages.success(request, 'Fee payment recorded successfully.')
            return redirect('fees:add_fee_payment')
    else:
        form = FeePaymentForm()
    return render(request, 'fees/add_fee_payment.html', {'form': form})

def add_fee_reminder(request):
    if request.method == 'POST':
        form = FeeReminderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee reminder created successfully.')
            return redirect('fees:add_fee_reminder')
    else:
        form = FeeReminderForm()
    return render(request, 'fees/add_fee_reminder.html', {'form': form})
