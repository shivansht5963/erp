# erp/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import index, role_based_redirect # Import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'), 
    path('dashboard/', role_based_redirect, name='dashboard_redirect'),
    path('api/v1/', include('api.urls')),
    
    # App URLs
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('fees/', include('fees.urls', namespace='fees')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('students/', include('students.urls', namespace='students')),
]