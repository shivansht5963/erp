import os
import sys
import django
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp.settings")
django.setup()

from students.models import Student, Course, Department, Class
from fees.models import FeeCategory, FeeStructure, FeePayment, FeeReminder, FeeCategoryAmount

class FeeWorkflowTest(TestCase):
    def setUp(self):
        # Create test user (admin)
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        
        # Create test department and course
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        
        self.course = Course.objects.create(
            name='Bachelor of Computer Applications',
            code='BCA',
            duration_years=3
        )
        
        # Create a class
        self.class_obj = Class.objects.create(
            department=self.department,
            course=self.course,
            semester=3,
            section='A',
            academic_year='2023-24'
        )
        
        # Create a student
        self.student = Student.objects.create(
            user=self.admin_user,
            roll_number='BCA2023001',
            first_name='Test',
            last_name='Student',
            email='test.student@example.com',
            date_of_birth=date(2000, 1, 1),
            gender='M',
            category='GENERAL',
            course=self.course,
            semester=3,
            class_enrolled=self.class_obj
        )
        
        # Create fee category
        self.fee_category = FeeCategory.objects.create(
            name='Tuition Fee',
            description='Tuition fee for the semester'
        )
        
        # Create fee structure
        self.fee_structure = FeeStructure.objects.create(
            category=self.fee_category,
            academic_year='2023-24',
            semester=3,
            amount=50000.00,  # Default amount
            due_date=timezone.now().date() + timedelta(days=30)
        )
        
        # Create category-specific amounts
        FeeCategoryAmount.objects.create(
            fee_structure=self.fee_structure,
            category='GENERAL',
            amount=50000.00
        )
        
        FeeCategoryAmount.objects.create(
            fee_structure=self.fee_structure,
            category='SC',
            amount=25000.00
        )
        
        FeeCategoryAmount.objects.create(
            fee_structure=self.fee_structure,
            category='ST',
            amount=20000.00
        )
    
    def test_fee_calculation(self):
        """Test that fee calculation works correctly for different categories"""
        # Test GENERAL category (should be 50000)
        self.student.category = 'GENERAL'
        self.student.save()
        amount = self.fee_structure.get_amount_for_category('GENERAL')
        self.assertEqual(amount, 50000.00)
        
        # Test SC category (should be 25000)
        self.student.category = 'SC'
        self.student.save()
        amount = self.fee_structure.get_amount_for_category('SC')
        self.assertEqual(amount, 25000.00)
        
        # Test ST category (should be 20000)
        self.student.category = 'ST'
        self.student.save()
        amount = self.fee_structure.get_amount_for_category('ST')
        self.assertEqual(amount, 20000.00)
        
        # Test non-existent category (should return default amount)
        amount = self.fee_structure.get_amount_for_category('NON_EXISTENT')
        self.assertEqual(amount, 50000.00)
    
    def test_fee_payment_workflow(self):
        """Test the complete fee payment workflow"""
        # Get fee summary before payment
        summary = FeePayment.get_student_fee_summary(self.student)
        self.assertEqual(summary['total_fees'], 50000.00)
        self.assertEqual(summary['amount_paid'], 0)
        self.assertEqual(summary['amount_due'], 50000.00)
        self.assertEqual(summary['fee_status'], 'unpaid')
        
        # Make a partial payment
        payment = FeePayment.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            amount=20000.00,
            payment_date=timezone.now().date(),
            payment_method='cash',
            created_by=self.admin_user
        )
        
        # Check fee summary after partial payment
        summary = FeePayment.get_student_fee_summary(self.student)
        self.assertEqual(summary['amount_paid'], 20000.00)
        self.assertEqual(summary['amount_due'], 30000.00)
        self.assertEqual(summary['fee_status'], 'partial')
        self.assertEqual(len(summary['recent_payments']), 1)
        
        # Make final payment
        FeePayment.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            amount=30000.00,
            payment_date=timezone.now().date(),
            payment_method='card',
            created_by=self.admin_user
        )
        
        # Check fee summary after full payment
        summary = FeePayment.get_student_fee_summary(self.student)
        self.assertEqual(summary['amount_paid'], 50000.00)
        self.assertEqual(summary['amount_due'], 0)
        self.assertEqual(summary['fee_status'], 'paid')
        self.assertEqual(len(summary['recent_payments']), 2)
    
    def test_fee_reminder_workflow(self):
        """Test the fee reminder workflow"""
        # Create a payment that's due soon
        fee_structure = FeeStructure.objects.create(
            category=self.fee_category,
            academic_year='2023-24',
            semester=3,
            amount=50000.00,
            due_date=timezone.now().date() + timedelta(days=5)  # Due in 5 days
        )
        
        # Create a reminder
        reminder = FeeReminder.objects.create(
            student=self.student,
            reminder_date=timezone.now().date(),
            subject='Fee Payment Reminder',
            message='This is a test reminder for fee payment.',
            created_by=self.admin_user
        )
        
        # Send the reminder
        result = reminder.send_reminder()
        self.assertTrue(result)
        self.assertTrue(reminder.sent)
        self.assertIsNotNone(reminder.sent_date)
        
        # Check that email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Fee Payment Reminder', mail.outbox[0].subject)
        self.assertIn(self.student.email, mail.outbox[0].to)
