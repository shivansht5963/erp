import secrets
import string
from django import forms
from students.models import Student
from accounts.models import CustomUser

class StudentWithUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Student
        fields = ['roll_number', 'course', 'semester', 'dob', 'contact_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        if self.instance and self.instance.pk:
            user = self.instance.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            student = super().save(commit=False)
            student.user = user
        else:
            password = ''.join(secrets.choice(string.ascii_letters + string.digits + '@_') for _ in range(12))
            user = CustomUser.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=password,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                role='student'
            )
            student = super().save(commit=False)
            student.user = user
            self._saved_password = password
        if commit:
            student.save()
        return student