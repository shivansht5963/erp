from django import forms
from accounts.models import CustomUser
from .models import Teacher, Department, Course, Class
import string
import secrets

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + '@_'
    return ''.join(secrets.choice(chars) for _ in range(length))
class TeacherWithUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Teacher
        fields = ['department', 'qualification', 'contact_number', 'join_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Editing: populate user fields from linked user
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        import secrets, string
        if self.instance and self.instance.pk:
            # Update existing user
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            teacher = super().save(commit=False)
            teacher.user = user
        else:
            # Create new user
            password = ''.join(secrets.choice(string.ascii_letters + string.digits + '@_') for _ in range(12))
            user = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=password,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='faculty'
            )
            teacher = super().save(commit=False)
            teacher.user = user
            self._saved_password = password
        if commit:
            teacher.save()
        return teacher