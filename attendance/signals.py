
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Attendance, AttendanceReport

@receiver(post_save, sender=Attendance)
def update_attendance_report_on_save(sender, instance, created, **kwargs):
    """
    This function is triggered every time an Attendance object is saved.
    It automatically finds the related AttendanceReport and updates its values.
    """
    # Find the corresponding report for the student and subject.
    # If it doesn't exist, create it. This is a very robust pattern.
    report, _ = AttendanceReport.objects.get_or_create(
        student=instance.student,
        subject=instance.subject
    )

    # Recalculate the totals directly from the source of truth: the Attendance model.
    total_classes = Attendance.objects.filter(student=instance.student, subject=instance.subject).count()
    classes_attended = Attendance.objects.filter(student=instance.student, subject=instance.subject, status=True).count()

    # Update the report fields.
    report.total_classes = total_classes
    report.classes_attended = classes_attended
    
    # Save the report. This will automatically call the .calculate_attendance()
    # method inside the AttendanceReport model, updating the percentage.
    report.save()

@receiver(post_delete, sender=Attendance)
def update_attendance_report_on_delete(sender, instance, **kwargs):
    """
    This function is triggered every time an Attendance object is deleted.
    It ensures the report is also updated if a record is removed by an admin.
    """
    # The logic is the same as saving, so we can just call the other handler.
    update_attendance_report_on_save(sender, instance, created=False, **kwargs)