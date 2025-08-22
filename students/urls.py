# students/urls.py

from django.urls import path
from .views import add_student, student_dashboard

app_name = 'students'

urlpatterns = [
    # URL for the new student dashboard
    path('dashboard/', student_dashboard, name='student_dashboard'),
    
    # Original URL for adding a student
    path('add/', add_student, name='add_student'),
]