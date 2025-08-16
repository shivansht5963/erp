
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from .models import Teacher, Department, Course, Class
from django.db import transaction

class TeacherRegistrationForm(UserCreationForm):
    """
    A form for creating a new teacher, which includes creating a CustomUser
    account and the related Teacher profile in one step.
    """
    # Adding fields for the Teacher model
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    qualification = forms.CharField(max_length=100, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    join_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2030)))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Fields for the CustomUser part of the form
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)

    @transaction.atomic
    def save(self, commit=True):
        # First, save the user part of the form
        user = super().save(commit=False)
        user.role = 'faculty'  # Set the role to faculty
        if commit:
            user.save()
            # Now, create and save the Teacher profile linked to this user
            Teacher.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                qualification=self.cleaned_data['qualification'],
                contact_number=self.cleaned_data['contact_number'],
                join_date=self.cleaned_data['join_date']
            )
        return user


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'