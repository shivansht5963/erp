from django.urls import path
from .views import create_teacher_notification, check_new_notifications, mark_all_read

# This sets the namespace for the app, allowing you to use names like 'notifications:create_teacher_notification'
app_name = 'notifications'

urlpatterns = [
    # This URL will be accessible at /notifications/teacher/create/
    path('teacher/create/', create_teacher_notification, name='create_teacher_notification'),
    path('check-new/', check_new_notifications, name='check_new'),
    path('mark-all-read/', mark_all_read, name='mark_all_read'),
]