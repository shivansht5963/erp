from django import forms
from .models import Attendance, AttendanceReport

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceReportForm(forms.ModelForm):
    class Meta:
        model = AttendanceReport
        fields = '__all__'
