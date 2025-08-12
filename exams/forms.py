from django import forms
from .models import Subject, Marks

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = '__all__'
