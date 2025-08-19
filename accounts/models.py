# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def login(self):
        """Method for login functionality"""
        return self.is_active
    
    def logout(self):
        """Method for logout functionality"""
        pass

class Notification(models.Model):
    # The student who will RECEIVE the notification.
    # This is now optional if sending to all students.
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        limit_choices_to={'role': 'student'}, # Ensures you can only select students
        blank=True, # Make this field optional in forms
        null=True   # Allow the database to store it as empty (NULL)
    )
    
    # The new checkbox for sending a broadcast message.
    send_to_all_students = models.BooleanField(
        default=False,
        help_text="Check this box to send the notification to ALL students."
    )

    # The admin or faculty who CREATED the notification.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_notifications'
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.send_to_all_students:
            return f"To ALL STUDENTS: {self.title}"
        # Handle cases where a specific recipient might not be selected
        if self.recipient:
            return f"To: {self.recipient.email} - {self.title}"
        return f"Draft Notification: {self.title}"


    class Meta:
        ordering = ['-created_at']