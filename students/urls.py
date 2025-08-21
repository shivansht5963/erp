# students/urls.py
from django.urls import path
from .views import add_student, student_dashboard

app_name = 'students'

from .views import dismiss_fee_reminder

urlpatterns = [
    path('add/', add_student, name='add_student'),
    # URL for the student dashboard view
    path('dashboard/', student_dashboard, name='dashboard'),
    path('dismiss_fee_reminder/', dismiss_fee_reminder, name='dismiss_fee_reminder'),
]