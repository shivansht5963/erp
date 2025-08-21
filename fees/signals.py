from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import FeePayment, FeeCategory
from .utils import send_fee_receipt
from students.models import Student

@receiver(post_save, sender=FeePayment)
def send_fee_payment_receipt(sender, instance, created, **kwargs):
    """
    Send a receipt email when a new fee payment is created.
    """
    if created and instance.amount > 0:
        # Only send receipt if email is configured
        if hasattr(settings, 'SEND_EMAILS') and settings.SEND_EMAILS:
            send_fee_receipt(instance)

@receiver(post_save, sender=FeePayment)
def create_fee_payment_reminder(sender, instance, created, **kwargs):
    """
    Create a reminder for the next payment if the current payment is partial.
    """
    if created:
        fee_summary = FeePayment.get_student_fee_summary(instance.student)
        
        # If there's still an amount due, create a reminder for 7 days from now
        if fee_summary['amount_due'] > 0:
            from .models import FeeReminder
            from django.utils import timezone
            
            # Check if there's already a pending reminder for this student
            existing_reminder = FeeReminder.objects.filter(
                student=instance.student,
                sent=False,
                reminder_date__gte=timezone.now().date()
            ).exists()
            
            if not existing_reminder:
                # Create a reminder for 7 days from now
                reminder_date = timezone.now().date() + timezone.timedelta(days=7)
                
                FeeReminder.objects.create(
                    student=instance.student,
                    reminder_date=reminder_date,
                    subject=f"Reminder: Outstanding Fee Balance of ₹{fee_summary['amount_due']:.2f}",
                    message=(
                        f"This is a reminder that you have an outstanding balance of ₹{fee_summary['amount_due']:.2f} "
                        f"for Course: {instance.fee_structure.course.name}, Category: {instance.student.category}. "
                        "Please make the payment at your earliest convenience to avoid any late fees or service interruptions.\n\n"
                        "You can make the payment through the student portal or by visiting the accounts office.\n\n"
                        "Thank you for your prompt attention to this matter."
                    ),
                    created_by=instance.created_by
                )
