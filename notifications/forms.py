from django import forms
from students.models import Student
from faculty.models import Class, Teacher # Make sure Teacher is imported

# This is the form for the Admin Panel
class AdminNotificationForm(forms.Form):
    TARGET_CHOICES = [
        ('all_students', 'All Students'),
        ('class', 'A Specific Class'),
        ('student', 'A Specific Student'),
    ]
    
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    target_type = forms.ChoiceField(choices=TARGET_CHOICES)
    target_class = forms.ModelChoiceField(
        queryset=Class.objects.all(), 
        required=False, 
        help_text="Select a class if targeting a specific class."
    )
    target_student = forms.ModelChoiceField(
        queryset=Student.objects.all(), 
        required=False, 
        help_text="Select a student if targeting a specific student."
    )

# THIS IS THE MISSING FORM FOR THE TEACHER VIEW
class TeacherNotificationForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    message = forms.CharField(widget=forms.Textarea())
    target_class = forms.ModelChoiceField(queryset=Class.objects.none(), label="Select Class")

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if teacher:
            # Logic to find the classes taught by a specific teacher
            teacher_classes = Class.objects.filter(department=teacher.department)
            self.fields['target_class'].queryset = teacher_classes