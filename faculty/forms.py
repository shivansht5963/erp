from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser
from .models import Teacher, Department, Course, Class

# class TeacherRegistrationForm(UserCreationForm):
#     department = forms.CharField(max_length=100)
#     qualification = forms.CharField(max_length=100)
#     contact_number = forms.CharField(max_length=15)
#     join_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1980, 2030)))

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'teacher'
#         if commit:
#             user.save()
#             Teacher.objects.create(
#                 user=user,
#                 department=self.cleaned_data['department'],
#                 qualification=self.cleaned_data['qualification'],
#                 contact_number=self.cleaned_data['contact_number'],
#                 join_date=self.cleaned_data['join_date']
#             )
#         return user

# class DepartmentForm(forms.ModelForm):
#     class Meta:
#         model = Department
#         fields = '__all__'

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'

# class ClassForm(forms.ModelForm):
#     class Meta:
#         model = Class
#         fields = '__all__'

# class TeacherForm(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = '__all__'

class TeacherWithUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Teacher
        fields = [
            'department',
            'qualification', 'contact_number', 'join_date'
        ]

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='faculty'
        )
        teacher = super().save(commit=False)
        teacher.user = user
        if commit:
            teacher.save()
        return teacher
