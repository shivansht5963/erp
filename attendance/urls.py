# attedance/urls.py
from django.urls import path
from .views import add_attendance, add_attendance_report, mark_attendance_for_subject

app_name = 'attendance'

urlpatterns = [
	path('add/', add_attendance, name='add_attendance'),
	path('add_report/', add_attendance_report, name='add_attendance_report'),
	   path('mark/<int:subject_id>/', mark_attendance_for_subject, name='mark_attendance'),
]