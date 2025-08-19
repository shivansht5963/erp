from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    # --- ADD THESE TWO FIELDS TO FIX THE CLASHING ERROR ---
    # We are overriding the default fields from AbstractUser to provide
    # a unique related_name. This tells Django how to create the "backwards"
    # relationship from Group and Permission to your CustomUser model without
    # conflicting with the built-in User model.
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups",  # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions",  # Unique related_name
        related_query_name="user",
    )
    
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