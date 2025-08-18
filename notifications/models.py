# notifications/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['faculty', 'admin']}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # We use a ManyToManyField to link a single notification to multiple users
    # The 'through' model lets us store extra info about the relationship (like is_read)
    recipients = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserNotificationStatus',
        related_name='notifications'
    )

    def __str__(self):
        return self.title

class UserNotificationStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        # Ensures a user can't be in the recipient list twice for the same notification
        unique_together = ('user', 'notification')

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.user.email} - {'Read' if self.is_read else 'Unread'}: {self.notification.title}"