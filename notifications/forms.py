# notifications/forms.py

from django import forms
from faculty.models import Class
from students.models import Student

class NotificationForm(forms.Form):
    AUDIENCE_CHOICES_ADMIN = [
        ('all_students', 'All Students'),
        ('class', 'A Specific Class'),
        ('student', 'A Specific Student'),
    ]
    
    AUDIENCE_CHOICES_FACULTY = [
        ('class', 'A Specific Class'),
    ]

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))
    
    # These fields will be shown/hidden with JavaScript
    audience_type = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    target_class = forms.ModelChoiceField(queryset=Class.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    target_student = forms.ModelChoiceField(queryset=Student.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user.role == 'admin':
            self.fields['audience_type'].choices = self.AUDIENCE_CHOICES_ADMIN
            self.fields['target_class'].queryset = Class.objects.all().order_by('department', 'semester')
            self.fields['target_student'].queryset = Student.objects.all().select_related('user').order_by('roll_number')
        
        elif user.role == 'faculty':
            self.fields['audience_type'].choices = self.AUDIENCE_CHOICES_FACULTY
            # This is a bit complex: find classes a teacher teaches in.
            # A simpler approach for now is to let them select from their department.
            # For a more robust solution, you'd trace subjects->teacher.
            teacher_profile = user.teacher
            self.fields['target_class'].queryset = Class.objects.filter(department=teacher_profile.department)