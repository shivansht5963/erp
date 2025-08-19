from django.urls import path
from .views import create_teacher_notification

# This sets the namespace for the app, allowing you to use names like 'notifications:create_teacher_notification'
app_name = 'notifications'

urlpatterns = [
    # This URL will be accessible at /notifications/teacher/create/
    path('teacher/create/', create_teacher_notification, name='create_teacher_notification'),
]