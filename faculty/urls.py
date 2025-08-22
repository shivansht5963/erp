# faculty/urls.py

from django.urls import path
from . import views
from .views import add_department, add_course, add_class, add_teacher
app_name = 'faculty'

urlpatterns = [
    # URLs for the new teacher dashboard workflow
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('class/<int:subject_id>/', views.class_detail, name='class_detail'),
    path('class/<int:subject_id>/mark_attendance/', views.mark_attendance_for_class, name='mark_attendance_for_class'),
    path('class/<int:subject_id>/save_marks/', views.save_marks_for_class, name='save_marks_for_class'),
    # Original URLs
    path('register/', views.register_teacher, name='register_teacher'),
    path('add_department/', add_department, name='add_department'),
    path('add_course/', add_course, name='add_course'),
    path('add_class/', add_class, name='add_class'),
    path('add_teacher/', add_teacher, name='add_teacher'),
]