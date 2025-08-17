# File: erp/urls.py

"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from .views import index  # Import the index view from erp/views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Define the root URL and name it 'home'. This is where users will be redirected.
    path('', index, name='home'),
    
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('students/', include('students.urls', namespace='students')),
]