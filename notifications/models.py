from django.db import models
from django.conf import settings
from students.models import Student
from faculty.models import Class

class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_notifications'
    )
    recipient = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'To: {self.recipient.user.username} - "{self.title}"'
    
    class Meta:
        ordering = ['-created_at']

# The NotificationSender proxy model has been deleted from this file.