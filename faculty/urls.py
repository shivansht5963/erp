from django.urls import path
from . import views
from .views import add_department, add_course, add_class, add_teacher

app_name = 'faculty'

urlpatterns = [
    # New URLs for teacher dashboard and marking attendance
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('subject/<int:subject_id>/attendance/', views.mark_attendance, name='mark_attendance'),

    # Existing URLs
    path('register/', views.register_teacher, name='register_teacher'),
    path('add_department/', add_department, name='add_department'),
    path('add_course/', add_course, name='add_course'),
    path('add_class/', add_class, name='add_class'),
    path('add_teacher/', add_teacher, name='add_teacher'),
]