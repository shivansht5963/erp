# File: erp/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # The root URL now correctly points to your main homepage.
    path('', views.index, name='home'),

    # This is the new, dedicated URL for our post-login dispatcher.
    # It matches the name we set in settings.py
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('students/', include('students.urls', namespace='students')),
]