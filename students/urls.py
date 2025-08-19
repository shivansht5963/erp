from django.urls import path
from .views import add_student, student_dashboard # Import the new view

app_name = 'students'
urlpatterns = [
    path('add/', add_student, name='add_student'),
    path('dashboard/', student_dashboard, name='student_dashboard'), # Add this line
]