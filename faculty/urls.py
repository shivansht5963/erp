from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    # New URLs for teacher dashboard and marking attendance
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('subject/<int:subject_id>/attendance/', views.mark_attendance, name='mark_attendance'),

    # Existing URLs for admin actions
    path('register/', views.register_teacher, name='register_teacher'),
    path('add_department/', views.add_department, name='add_department'),
    path('add_course/', views.add_course, name='add_course'),
    path('add_class/', views.add_class, name='add_class'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
]