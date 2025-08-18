from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
# Import the Department model to use in the form
from .models import Teacher, Department, Course, Class

class TeacherRegistrationForm(UserCreationForm):
    # --- THIS IS THE FIX ---
    # Use ModelMultipleChoiceField to allow selecting multiple departments
    departments = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple, # A checkbox list is user-friendly
        label="Departments"
    )
    qualification = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    join_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2030)))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'faculty'
        if commit:
            user.save()
            # Create the teacher profile first
            teacher = Teacher.objects.create(
                user=user,
                qualification=self.cleaned_data['qualification'],
                contact_number=self.cleaned_data['contact_number'],
                join_date=self.cleaned_data['join_date']
            )
            # Then, set the many-to-many relationship
            teacher.departments.set(self.cleaned_data['departments'])
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