from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .models import FeeReminder, FeePayment

def create_fee_reminder(student, subject=None, message=None, reminder_date=None, created_by=None):
    """
    Create a fee reminder for a student
    
    Args:
        student: Student instance
        subject: Reminder subject (optional, will be generated if not provided)
        message: Reminder message (optional, will be generated if not provided)
        reminder_date: Date to send the reminder (defaults to tomorrow)
        created_by: User who created the reminder (defaults to None for system)
        
    Returns:
        FeeReminder instance
    """
    # Get fee summary for the student
    fee_summary = FeePayment.get_student_fee_summary(student)
    
    # Set default values if not provided
    if reminder_date is None:
        reminder_date = timezone.now().date() + timezone.timedelta(days=1)
    
    if subject is None:
        if fee_summary['amount_due'] > 0:
            subject = f"Fee Payment Reminder - ₹{fee_summary['amount_due']} Pending"
        else:
            subject = "Fee Payment Confirmation"
    
    if message is None:
        if fee_summary['amount_due'] > 0:
            message = (
                f"Dear {student.user.get_full_name()},\n\n"
                f"This is a reminder that you have a pending fee payment of ₹{fee_summary['amount_due']}. "
                "Please make the payment at your earliest convenience to avoid any late fees or penalties.\n\n"
                "You can view your fee details and payment history in your student portal.\n\n"
                "Thank you for your prompt attention to this matter.\n\n"
                "Best regards,\n"
                f"{settings.SCHOOL_NAME or 'School'} Administration"
            )
        else:
            message = (
                f"Dear {student.user.get_full_name()},\n\n"
                "This is a confirmation that your fee payment has been received. "
                "Thank you for your prompt payment.\n\n"
                "You can view your payment details in your student portal.\n\n"
                "Best regards,\n"
                f"{settings.SCHOOL_NAME or 'School'} Administration"
            )
    
    # Create the reminder
    reminder = FeeReminder.objects.create(
        student=student,
        subject=subject,
        message=message,
        reminder_date=reminder_date,
        created_by=created_by
    )
    
    return reminder

def send_fee_receipt(payment, request=None):
    """
    Send a fee payment receipt to the student
    
    Args:
        payment: FeePayment instance
        request: HttpRequest object (optional, for building absolute URLs)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not payment.student.user.email:
        return False
    
    context = {
        'payment': payment,
        'student': payment.student,
        'fee_structure': payment.fee_structure,
        'school_name': getattr(settings, 'SCHOOL_NAME', 'School'),
    }
    
    # Add absolute URL for receipt if request is provided
    if request is not None:
        from django.urls import reverse
        context['receipt_url'] = request.build_absolute_uri(
            reverse('admin:fees_feepayment_change', args=[payment.id])
        )
    
    subject = f"Fee Payment Receipt - {payment.transaction_id or 'No Transaction ID'}"
    
    try:
        html_message = render_to_string('fees/email/fee_receipt.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payment.student.user.email],
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error sending fee receipt email: {str(e)}", exc_info=True)
        return False

def get_student_fee_summary(student):
    """
    Get a summary of a student's fee status
    
    Args:
        student: Student instance
        
    Returns:
        dict: Contains total_fees, amount_paid, amount_due, and fee_status
    """
    return FeePayment.get_student_fee_summary(student)
