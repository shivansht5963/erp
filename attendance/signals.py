

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Attendance, AttendanceReport

@receiver(post_save, sender=Attendance)
def update_attendance_report_on_save(sender, instance, created, **kwargs):
    """
    Updates the AttendanceReport whenever an Attendance record is created or updated.
    """
    report, _ = AttendanceReport.objects.get_or_create(
        student=instance.student,
        subject=instance.subject
    )
    
    total_classes = Attendance.objects.filter(student=instance.student, subject=instance.subject).count()
    classes_attended = Attendance.objects.filter(student=instance.student, subject=instance.subject, status=True).count()
    
    report.total_classes = total_classes
    report.classes_attended = classes_attended
    report.save() # This will trigger the calculate_attendance method in the model

@receiver(post_delete, sender=Attendance)
def update_attendance_report_on_delete(sender, instance, **kwargs):
    """
    Updates the AttendanceReport whenever an Attendance record is deleted.
    """
    update_attendance_report_on_save(sender, instance, created=False, **kwargs)