"""
URL configuration for erp project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.index, name='home'), 

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('students/', include('students.urls', namespace='students')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]