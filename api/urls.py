# File: api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register all viewsets
router = DefaultRouter()

# Student endpoints
router.register(r'students', views.StudentViewSet, basename='student')

# Faculty endpoints
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'classes', views.ClassViewSet, basename='class')
router.register(r'teachers', views.TeacherViewSet, basename='teacher')

# Attendance endpoints
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')

# Fees endpoints
router.register(r'fees/payments', views.FeePaymentViewSet, basename='fee-payment')

# Marks endpoints
router.register(r'marks', views.MarksViewSet, basename='marks')

# Results endpoints
router.register(r'results', views.ResultViewSet, basename='results')

# Authentication endpoints
router.register(r'auth', views.AuthViewSet, basename='auth')

# Notification endpoints
router.register(r'notifications', views.NotificationViewSet, basename='notification')

# Include router URLs
urlpatterns = [
    path('', include(router.urls)),
]