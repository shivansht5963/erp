

from django import forms
from .models import Student

# This file should ONLY import from Django and your models.py, not views.py.

class StudentForm(forms.ModelForm):
    """
    A form for creating and updating Student profiles. This form is used by an
    admin in a view like `add_student`.
    """
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Birth"
    )

    class Meta:
        model = Student
        # The fields from the Student model to include in the form.
        fields = [
            'roll_number',
            'course',
            'semester',
            'dob',
            'contact_number',
            'address'
        ]