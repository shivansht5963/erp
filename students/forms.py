

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth"
    )
    class Meta:
        model = Student
        # Add 'class_assigned' to the list of fields.
        fields = ['roll_number', 'class_assigned', 'course', 'semester', 'dob', 'contact_number']