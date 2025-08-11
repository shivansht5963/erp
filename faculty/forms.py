from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from .models import Teacher

class TeacherRegistrationForm(UserCreationForm):
    department = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    join_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2030)))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
            Teacher.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                qualification=self.cleaned_data['qualification'],
                contact_number=self.cleaned_data['contact_number'],
                join_date=self.cleaned_data['join_date']
            )
        return user
