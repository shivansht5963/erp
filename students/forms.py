from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # calendar picker
        label="Date of Birth"
    )
    class Meta:
        model = Student
        fields = ['roll_number', 'course', 'semester', 'dob', 'contact_number']
