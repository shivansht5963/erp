# attedance/urls.py
from django.urls import path

app_name = 'attendance'

urlpatterns = []
from .views import add_attendance, add_attendance_report

urlpatterns = [
	path('add/', add_attendance, name='add_attendance'),
	path('add_report/', add_attendance_report, name='add_attendance_report'),
]