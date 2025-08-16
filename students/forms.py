from django import forms
from students.models import Student
from accounts.models import CustomUser

class StudentWithUserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Student
        fields = ['roll_number', 'course', 'semester', 'dob', 'contact_number', 'address']

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            role='student'
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student