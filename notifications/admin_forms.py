# notifications/admin_forms.py

from django import forms
from .models import Notification
from faculty.models import Class

class NotificationAdminForm(forms.ModelForm):
    """
    A custom form for creating Notifications within the Django Admin.
    Includes a field to select the target class.
    """
    target_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label="Send to Class",
        help_text="Select the class that should receive this notification."
    )

    class Meta:
        model = Notification
        fields = ('title', 'message', 'target_class')

    def __init__(self, *args, **kwargs):
        # We receive the 'request' object from the admin to get the current user
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # If the user is a teacher, filter the class choices to only their departments
        if request and request.user.role == 'faculty':
            teacher = getattr(request.user, 'teacher', None)
            if teacher:
                teacher_departments = teacher.departments.all()
                self.fields['target_class'].queryset = Class.objects.filter(department__in=teacher_departments)