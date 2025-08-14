
from django.urls import path
# --- IMPORT THE NEW VIEW ---
from .views import add_student, student_dashboard

app_name = 'students'

urlpatterns = [
    # This URL is for an admin to add a student
    path('add/', add_student, name='add_student'),
    
    # --- ADD THIS CRUCIAL LINE ---
    # This maps the URL '/students/dashboard/' to the 'student_dashboard' view
    # and gives it the name 'student_dashboard', which matches your settings.
    path('dashboard/', student_dashboard, name='student_dashboard'),
]