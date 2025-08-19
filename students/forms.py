# students/forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # calendar picker
        label="Date of Birth"
    )
    class Meta:
        model = Student
        # Added 'class_enrolled' and 'address' to the form fields
        fields = ['roll_number', 'course', 'class_enrolled', 'semester', 'dob', 'contact_number', 'address']