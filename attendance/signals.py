# attendance/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AttendanceReport
from accounts.models import Notification

@receiver(post_save, sender=AttendanceReport)
def create_low_attendance_notification(sender, instance, **kwargs):
    """
    Creates a notification for a student if their attendance percentage
    for a subject is below 75%.
    """
    # Check if the attendance is below the threshold
    if instance.attendance_percentage < 75.0:
        # Define a unique message to prevent duplicates
        message = f"Your attendance for {instance.subject.name} is now {instance.attendance_percentage:.2f}%. Please improve your attendance."
        
        # Check if an identical unread notification already exists
        notification_exists = Notification.objects.filter(
            user=instance.student.user,
            title='Low Attendance Alert',
            message=message,
            read=False
        ).exists()

        if not notification_exists:
            Notification.objects.create(
                user=instance.student.user,
                title='Low Attendance Alert',
                message=message
            )