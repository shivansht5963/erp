# notifications/urls.py

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # For Admins/Faculty to send notifications
    path('create/', views.create_notification, name='create'),
    
    # For Students to view their notifications
    path('list/', views.notification_list, name='list'),
    
    # To mark a notification as read
    path('mark-read/<int:status_id>/', views.mark_notification_as_read, name='mark_as_read'),
]