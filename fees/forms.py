from django import forms
from .models import FeeCategory, FeeStructure, FeePayment, FeeReminder

class FeeCategoryForm(forms.ModelForm):
    class Meta:
        model = FeeCategory
        fields = '__all__'

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = '__all__'

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = '__all__'

class FeeReminderForm(forms.ModelForm):
    class Meta:
        model = FeeReminder
        fields = '__all__'
