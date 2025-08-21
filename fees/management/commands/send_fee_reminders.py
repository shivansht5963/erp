import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from fees.models import FeeReminder, FeePayment
from students.models import Student

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends fee payment reminders to students with pending or overdue payments'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Send reminders even if they have already been sent',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate sending reminders without actually sending them',
        )
    
    def handle(self, *args, **options):
        force = options.get('force', False)
        dry_run = options.get('dry_run', False)
        
        # Get all unsent reminders that are due
        reminder_filter = Q(reminder_date__lte=timezone.now().date())
        if not force:
            reminder_filter &= Q(sent=False)
            
        due_reminders = FeeReminder.objects.filter(reminder_filter)\
            .select_related('student__user')\
            .order_by('reminder_date')

        if not due_reminders.exists():
            self.stdout.write(self.style.SUCCESS('No fee reminders to send at this time.'))
            return

        self.stdout.write(f'Processing {due_reminders.count()} fee reminders...')
        
        success_count = 0
        error_count = 0
        
        for reminder in due_reminders:
            try:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(
                            f'[DRY RUN] Would send reminder to {reminder.student} ({reminder.student.roll_number}) - {reminder.subject}'
                        )
                    )
                    success_count += 1
                    continue
                
                if reminder.send_reminder():
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Sent reminder to {reminder.student} ({reminder.student.roll_number}) - {reminder.subject}'
                        )
                    )
                else:
                    error_count += 1
                    self.stderr.write(
                        self.style.ERROR(
                            f'Failed to send reminder to {reminder.student} ({reminder.student.roll_number}) - {reminder.subject}'
                        )
                    )
                    
            except Exception as e:
                error_count += 1
                logger.error(
                    f'Error sending fee reminder {reminder.id}: {str(e)}',
                    exc_info=True
                )
                self.stderr.write(
                    self.style.ERROR(
                        f'Error processing reminder {reminder.id}: {str(e)}'
                    )
                )

        if dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'[DRY RUN] Would have sent {success_count} fee reminders with {error_count} errors.'
            ))
        elif success_count > 0 or error_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully sent {success_count} fee reminders with {error_count} errors.'
            ))
        else:
            self.stdout.write('No fee reminders were processed.')
            
        # If no reminders were found, check for students who might need reminders
        if not due_reminders.exists() and not dry_run:
            self.stdout.write('\nChecking for students who might need fee reminders...')
            self.check_students_needing_reminders()
    
    def check_students_needing_reminders(self):
        """
        Identifies students who have pending fee payments but no active reminders
        and creates reminders for them.
        """
        current_year = timezone.now().year
        academic_year = f"{current_year}-{current_year + 1}"
        
        # Get all active fee structures
        fee_structures = FeeStructure.objects.filter(
            is_active=True,
            academic_year=academic_year
        )
        
        if not fee_structures.exists():
            self.stdout.write(self.style.WARNING('No active fee structures found for the current academic year.'))
            return
        
        # Get all students with pending payments
        students_with_payments = Student.objects.filter(
            fee_payments__fee_structure__in=fee_structures
        ).distinct()
        
        # Get students who already have active reminders
        students_with_reminders = Student.objects.filter(
            fee_reminders__sent=False,
            fee_reminders__reminder_date__gte=timezone.now().date()
        ).values_list('id', flat=True)
        
        # Find students who need reminders
        students_needing_reminders = students_with_payments.exclude(
            id__in=students_with_reminders
        )
        
        if students_needing_reminders.exists():
            self.stdout.write(f'Found {students_needing_reminders.count()} students who might need fee reminders.')
            self.stdout.write('You can create reminders for them using the admin interface.')
        else:
            self.stdout.write('No additional students need fee reminders at this time.')
