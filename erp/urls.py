# erp/urls.py

"""
URL configuration for erp project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Import the views from the current 'erp' directory

urlpatterns = [
    path('admin/', admin.site.urls),

    # Add the URL for our smart redirect view. This is the new entry point after login.
    path('login-redirect/', views.login_redirect, name='login_redirect'),

    # Include all your app-specific URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('students/', include('students.urls', namespace='students')),

    # Optional: A root path to your index page
    path('', views.index, name='home'),
]