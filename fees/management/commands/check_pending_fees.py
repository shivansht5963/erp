from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q, Sum
from students.models import Student
from fees.models import FeePayment, FeeReminder
from django.conf import settings

class Command(BaseCommand):
    help = 'Check for students with pending fees and generate reminders if needed'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the command without making any changes',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days in the future to set the reminder for (default: 7)',
        )
    
    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        days = options.get('days', 7)
        
        # Get current academic year (assuming format YYYY-YYYY)
        current_year = timezone.now().year
        academic_year = f"{current_year}-{current_year + 1}"
        
        self.stdout.write(self.style.SUCCESS(f'Checking for students with pending fees (Academic Year: {academic_year})...'))
        
        # Get all active students with fee payments in the current academic year
        students_with_fees = Student.objects.filter(
            fee_payments__fee_structure__academic_year=academic_year,
            is_active=True
        ).distinct()
        
        if not students_with_fees.exists():
            self.stdout.write(self.style.WARNING('No students with fee records found for the current academic year.'))
            return
        
        reminder_date = timezone.now().date() + timezone.timedelta(days=days)
        reminder_count = 0
        
        for student in students_with_fees:
            # Get fee summary for the student
            fee_summary = FeePayment.get_student_fee_summary(student)
            
            # Skip if no amount is due
            if fee_summary['amount_due'] <= 0:
                continue
                
            # Check if there's already a pending reminder for this student
            has_pending_reminder = FeeReminder.objects.filter(
                student=student,
                sent=False,
                reminder_date__gte=timezone.now().date()
            ).exists()
            
            if not has_pending_reminder:
                # Create a new reminder
                reminder = FeeReminder(
                    student=student,
                    reminder_date=reminder_date,
                    subject=f"Reminder: Outstanding Fee Balance of ₹{fee_summary['amount_due']:.2f}",
                    message=(
                        f"Dear {student.user.get_full_name() or student.user.username},\n\n"
                        f"This is a reminder that you have an outstanding balance of ₹{fee_summary['amount_due']:.2f} "
                        "for your tuition and other fees. "
                        "Please make the payment at your earliest convenience to avoid any late fees or service interruptions.\n\n"
                        "You can make the payment through the student portal or by visiting the accounts office.\n\n"
                        "Thank you for your prompt attention to this matter.\n\n"
                        f"Best regards,\n{getattr(settings, 'SCHOOL_NAME', 'School Administration')}"
                    ),
                    created_by=None  # System-generated
                )
                
                if not dry_run:
                    reminder.save()
                    reminder_count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created reminder for {student} (Due: ₹{fee_summary["amount_due"]:.2f}) - Reminder date: {reminder_date}'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'[DRY RUN] Would create reminder for {student} (Due: ₹{fee_summary["amount_due"]:.2f}) - Reminder date: {reminder_date}'
                    ))
                    reminder_count += 1
        
        if reminder_count == 0:
            self.stdout.write(self.style.SUCCESS('No new reminders needed at this time.'))
        else:
            action = 'Created' if not dry_run else 'Would create'
            self.stdout.write(self.style.SUCCESS(
                f'{action} {reminder_count} reminder(s) for students with pending fees.'
            )
            
            if not dry_run:
                # Get total pending amount across all students
                total_pending = sum(
                    FeePayment.get_student_fee_summary(s)['amount_due']
                    for s in students_with_fees
                )
                
                self.stdout.write(self.style.SUCCESS(
                    f'Total pending amount across all students: ₹{total_pending:,.2f}'
                ))
