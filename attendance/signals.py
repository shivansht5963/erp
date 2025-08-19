from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Attendance, AttendanceReport

def _update_attendance_report(student, subject):
    """
    A helper function to recalculate the aggregate attendance report.
    This is called when any daily attendance record is saved or deleted.
    """
    # Sum up all 'classes_held' for this student in this subject across all dates.
    total_held_agg = Attendance.objects.filter(student=student, subject=subject).aggregate(total=Sum('classes_held'))
    total_held = total_held_agg['total'] or 0

    # Sum up all 'classes_attended' for this student in this subject across all dates.
    total_attended_agg = Attendance.objects.filter(student=student, subject=subject).aggregate(total=Sum('classes_attended'))
    total_attended = total_attended_agg['total'] or 0

    # Find the summary report (or create it if it's the first entry)
    report, created = AttendanceReport.objects.get_or_create(
        student=student,
        subject=subject
    )
    
    # Update the report with the newly calculated totals
    report.total_classes = total_held
    report.classes_attended = total_attended
    report.save()  # This will trigger the percentage calculation in the report's own save method

@receiver(post_save, sender=Attendance)
def on_attendance_save(sender, instance, **kwargs):
    """
    Signal receiver that runs every time a daily Attendance record is created or updated.
    """
    _update_attendance_report(instance.student, instance.subject)
    print(f"Report updated for {instance.student} in {instance.subject} after save operation.")

@receiver(post_delete, sender=Attendance)
def on_attendance_delete(sender, instance, **kwargs):
    """
    Signal receiver that runs every time a daily Attendance record is deleted.
    """
    _update_attendance_report(instance.student, instance.subject)
    print(f"Report updated for {instance.student} in {instance.subject} after delete operation.")