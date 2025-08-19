# faculty/urls.py

from django.urls import path
from . import views
from .views import add_department, add_course, add_class, add_teacher

app_name = 'faculty'

urlpatterns = [
<<<<<<< HEAD
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'), # Add this line
=======
>>>>>>> 8c12e2bd7ac120195293f49c24993eeea4e2968b
    path('register/', views.register_teacher, name='register_teacher'),
    path('add_department/', add_department, name='add_department'),
    path('add_course/', add_course, name='add_course'),
    path('add_class/', add_class, name='add_class'),
    path('add_teacher/', add_teacher, name='add_teacher'),
]