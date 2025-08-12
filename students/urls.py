# students/urls.py
from django.urls import path
from .views import add_student

app_name = 'students'
urlpatterns = [
    path('add/', add_student, name='add_student'),
]