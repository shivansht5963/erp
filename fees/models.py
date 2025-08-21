from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, Q
from students.models import Student
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse

class FeeCategory(models.Model):
    """Student categories (General, SC/ST, OBC, etc.)"""
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('SCST', 'SC/ST'),
        ('TFWS', 'TFWS'),
        ('OBC', 'OBC'),
        ('EWS', 'EWS'),
        ('MINORITY', 'Minority'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_students(self):
        from students.models import Student
        return Student.objects.filter(category=self.name)

    def student_count(self):
        return self.get_students().count()
    class Meta:
        verbose_name_plural = 'Fee Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class FeeStructure(models.Model):
    """Defines the fee structure for different courses"""
    course = models.ForeignKey('faculty.Course', on_delete=models.CASCADE, related_name='fee_structures', help_text='Course this fee structure applies to')
    fee_type = models.CharField(max_length=100, help_text='Type of fee (Tuition, Library, Hostel, etc.)')
    academic_year = models.CharField(max_length=9, help_text='Format: YYYY-YYYY')
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Base fee amount')
    due_date = models.DateField()
    is_active = models.BooleanField(default=True, help_text='Whether this fee structure is currently active')
    
        
    def __str__(self):
        return f"{self.course.name} - {self.fee_type} ({self.academic_year}) - ₹{self.amount}"
        
    def get_amount_for_category(self, category):
        """
        Get the fee amount for a specific student category.
        
        Args:
            category (str): The student's category (e.g., 'SC', 'ST', 'GENERAL', etc.)
            
        Returns:
            Decimal: The fee amount for the specified category, or the default amount if not specified
        """
        # Try to get the category-specific amount from FeeCategoryAmount first
        try:
            category_amount = self.category_amounts.get(category=category)
            return category_amount.amount
        except FeeCategoryAmount.DoesNotExist:
            # If no specific amount is set for this category, use the default amount
            return self.amount
    
class FeeCategoryAmount(models.Model):
    """Stores different fee amounts for different student categories"""
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='category_amounts')
    category = models.CharField(
        max_length=20, 
        choices=Student.CATEGORY_CHOICES,
        help_text='Student category this fee applies to'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Fee amount for this category'
    )
    
    class Meta:
        unique_together = ('fee_structure', 'category')
        verbose_name_plural = 'Fee category amounts'
    
    def __str__(self):
        return f"{self.fee_structure.course.name} - {self.get_category_display()} - ₹{self.amount}"

class FeePayment(models.Model):
    """Tracks fee payments made by students"""
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('cheque', 'Cheque'),
        ('dd', 'Demand Draft'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        related_name='fee_payments',
        help_text='Student making the payment'
    )
    fee_structure = models.ForeignKey(
        FeeStructure, 
        on_delete=models.CASCADE, 
        related_name='payments',
        help_text='Fee structure this payment is for'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text='Amount being paid in this transaction'
    )
    payment_date = models.DateField(
        default=timezone.now,
        help_text='Date when payment was received'
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES,
        help_text='Method used for payment'
    )
    transaction_id = models.CharField(
        max_length=100, 
        blank=True,
        help_text='Transaction/Receipt number for reference'
    )
    remarks = models.TextField(
        blank=True,
        help_text='Any additional notes about this payment'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_payments',
        help_text='User who recorded this payment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = 'Fee Payment'
        verbose_name_plural = 'Fee Payments'
    
    def get_absolute_url(self):
        return reverse('admin:fees_feepayment_change', args=[self.id])
        
    def __str__(self):
        return f"{self.student.roll_number} - {self.fee_structure.course.name} - ₹{self.amount}"
        
    @classmethod
    def get_student_fee_summary(cls, student):
        """
        Get fee summary for a student including total fees, amount paid, pending amount,
        recent payments, and next due date.
        
        Returns:
            dict: A dictionary containing fee summary information with the following keys:
                - total_fees (Decimal): Total fees for the current semester
                - amount_paid (Decimal): Total amount paid
                - amount_due (Decimal): Remaining amount to be paid
                - fee_status (str): Payment status ('paid', 'partial', 'unpaid')
                - academic_year (str): Current academic year
                - semester (int): Current semester
                - recent_payments (QuerySet): Last 5 fee payments
                - next_due_date (date): Next due date for payment (if any)
        """
        current_year = timezone.now().year
        academic_year = f"{current_year}-{current_year + 1}"
        
        # Get all active fee structures for student's course and current academic year
        fee_structures = FeeStructure.objects.filter(
            course=student.course,
            academic_year=academic_year,
            is_active=True
        )
        
        if not fee_structures.exists():
            return {
                'total_fees': 0,
                'amount_paid': 0,
                'amount_due': 0,
                'fee_status': 'unpaid',
                'academic_year': academic_year,
                'semester': student.semester,
                'recent_payments': cls.objects.none(),
                'next_due_date': None
            }
        
        # Calculate total fees based on student's category
        total_fees = sum(
            fs.get_amount_for_category(student.category) 
            for fs in fee_structures
        )
        
        # Get all payments made by student for current fee structures
        payments = cls.objects.filter(
            student=student,
            fee_structure__in=fee_structures
        )
        
        # Calculate total amount paid
        total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
        
        # Get recent payments (last 5)
        recent_payments = payments.order_by('-payment_date', '-created_at')[:5]
        
        # Calculate amount due (can't be negative)
        amount_due = max(total_fees - total_paid, 0)
        
        # Determine fee status
        if total_paid >= total_fees:
            fee_status = 'paid'
        elif total_paid > 0:
            fee_status = 'partial'
        else:
            fee_status = 'unpaid'
        
        # Get next due date (earliest due date from fee structures that are not fully paid)
        next_due_date = None
        if amount_due > 0:
            next_due = fee_structures.filter(
                due_date__gte=timezone.now().date()
            ).order_by('due_date').first()
            
            if next_due:
                next_due_date = next_due.due_date
        
        return {
            'total_fees': total_fees,
            'amount_paid': total_paid,
            'amount_due': amount_due,
            'fee_status': fee_status,
            'academic_year': academic_year,
            'course': student.course.name,
            'recent_payments': recent_payments,
            'next_due_date': next_due_date
        }
    
    def create_or_update_reminder(self):
        """Create or update fee payment reminder"""
        days_until_due = (self.due_date - timezone.now().date()).days
        
        # Don't create reminders for paid or far future payments
        if self.payment_status == 'paid' or days_until_due > 30:
            return
            
        # If payment is overdue, create/update reminder for 1 day from now
        if self.is_overdue:
            reminder_date = timezone.now().date() + timezone.timedelta(days=1)
        # If due in less than 7 days, create/update reminder for tomorrow
        elif days_until_due <= 7:
            reminder_date = timezone.now().date() + timezone.timedelta(days=1)
        # Otherwise, create reminder for 7 days before due date
        else:
            reminder_date = self.due_date - timezone.timedelta(days=7)
        
        # Create or update reminder
        FeeReminder.objects.update_or_create(
            fee_payment=self,
            defaults={
                'reminder_date': reminder_date,
                'message': self.generate_reminder_message(),
                'sent': False
            }
        )
    
    def generate_reminder_message(self):
        """Generate a reminder message for this fee payment"""
        status = dict(self.PAYMENT_STATUS_CHOICES).get(self.payment_status, self.payment_status)
        return (
            f"Reminder: {self.fee_structure.name} - {self.get_category_display()} - "
            f"Amount: ₹{self.total_amount} | Due: {self.due_date} | Status: {status}"
        )
    
    def send_reminder_email(self):
        """Send reminder email to student"""
        if not self.student.user.email:
            return False
            
        subject = f"Fee Payment Reminder: {self.fee_structure.name}"
        context = {
            'student': self.student,
            'fee_payment': self,
            'amount_due': self.amount_due,
            'due_date': self.due_date,
            'payment_status': dict(self.PAYMENT_STATUS_CHOICES).get(self.payment_status, self.payment_status),
        }
        
        html_message = render_to_string('fees/email/fee_reminder.html', context)
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.student.user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.fee_structure.course.name} - ₹{self.amount}"

class FeeReminder(models.Model):
    """Tracks fee payment reminders sent to students"""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fee_reminders',
        help_text='Student who will receive the reminder'
    )
    reminder_date = models.DateField(
        default=timezone.now,
        help_text='Date when the reminder was/will be sent'
    )
    subject = models.CharField(
        max_length=200,
        help_text='Subject of the reminder email'
    )
    message = models.TextField(
        help_text='Reminder message content'
    )
    sent = models.BooleanField(
        default=False,
        help_text='Whether the reminder has been sent'
    )
    sent_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the reminder was actually sent'
    )
    amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Amount due for payment'
    )
    due_date = models.DateField(
        help_text='Due date for the payment'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_reminders',
        help_text='User who created this reminder'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reminder_date', '-created_at']
        verbose_name = 'Fee Reminder'
        verbose_name_plural = 'Fee Reminders'
    
    def __str__(self):
        return f"Reminder for {self.student} - {self.reminder_date}"
    
    def send_reminder(self):
        """Send the reminder email and update status"""
        if self.sent or not self.student.user.email:
            return False
            
        try:
            context = {
                'student': self.student,
                'reminder': self,
                'fee_summary': FeePayment.get_student_fee_summary(self.student)
            }
            
            html_message = render_to_string('fees/email/fee_reminder.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=self.subject,
                message=plain_message,
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.student.user.email],
                fail_silently=False,
            )
            
            self.sent = True
            self.sent_date = timezone.now()
            self.save()
            return True
            
        except Exception as e:
            print(f"Error sending reminder email: {e}")
            return False
