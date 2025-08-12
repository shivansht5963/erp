
from django.db import models
from django.utils import timezone
from students.models import Student

class FeeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Fee Categories"

class FeeStructure(models.Model):
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    semester = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    academic_year = models.CharField(max_length=9)  # Format: 2023-2024
    
    def __str__(self):
        return f"{self.category.name} - {self.course} - Semester {self.semester} - {self.academic_year}"

class FeePayment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('other', 'Other'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)
    
    def calculate_payment_status(self):
        if not self.amount_paid:
            if timezone.now().date() > self.fee_structure.due_date:
                return 'overdue'
            return 'pending'
        
        if self.amount_paid >= self.fee_structure.amount:
            return 'paid'
        else:
            if timezone.now().date() > self.fee_structure.due_date:
                return 'overdue'
            return 'partial'
    
    def save(self, *args, **kwargs):
        self.payment_status = self.calculate_payment_status()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student.roll_number} - {self.fee_structure.category.name} - {self.payment_status}"

class FeeReminder(models.Model):
    fee_payment = models.ForeignKey(FeePayment, on_delete=models.CASCADE)
    reminder_date = models.DateField()
    message = models.TextField()
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Reminder for {self.fee_payment.student.roll_number} - {self.reminder_date}"
