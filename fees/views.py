from django.shortcuts import render, redirect
from .forms import FeeCategoryForm, FeeStructureForm, FeePaymentForm, FeeReminderForm

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

def add_fee_reminder(request):
    if request.method == 'POST':
        form = FeeReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fees:add_fee_reminder')
    else:
        form = FeeReminderForm()
    return render(request, 'fees/add_fee_reminder.html', {'form': form})
