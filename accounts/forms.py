# File: accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Notification  # <-- Make sure Notification is imported
from django.core.exceptions import ValidationError # <-- Make sure this is imported

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

# --- START OF NEW CODE ---
# This is the form class that was missing.
class NotificationAdminForm(forms.ModelForm):
    class Meta:
        model = Notification
        # Ensure all fields from the model are included for the form to use
        fields = ('recipient', 'send_to_all_students', 'title', 'message', 'read')

    def clean(self):
        """
        Adds custom validation rules to the form.
        """
        cleaned_data = super().clean()
        recipient = cleaned_data.get('recipient')
        send_to_all = cleaned_data.get('send_to_all_students')

        # Rule 1: You must choose either a recipient OR the "send to all" checkbox.
        if not recipient and not send_to_all:
            raise ValidationError(
                "Validation Error: You must either select a specific student recipient or check the 'Send to all students' box."
            )
        
        # Rule 2: You cannot choose both at the same time.
        if recipient and send_to_all:
            raise ValidationError(
                "Validation Error: You cannot select a specific student AND check 'Send to all students'. Please choose only one option."
            )
            
        return cleaned_data
# --- END OF NEW CODE ---