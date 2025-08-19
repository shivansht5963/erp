

from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Student model.
    """
    # Define which fields to display in the list view.
    # We are using the correct field name 'class_assigned' here.
    list_display = (
        'roll_number',
        'user',
        'course',
        'semester',
        'class_assigned',  # Corrected from 'class_enrolled'
        'contact_number'
    )
    
    # Add filters to the right sidebar for easier navigation.
    list_filter = (
        'course',
        'semester',
        'class_assigned'   # Corrected from 'class_enrolled'
    )
    
    # Add a search bar that can search by roll number or user's name.
    search_fields = (
        'roll_number',
        'user__first_name',
        'user__last_name',
        'user__email'
    )
    
    # Make the user field a searchable dropdown for better performance.
    raw_id_fields = ('user',)

# Note: We are using the @admin.register decorator, so the line
# admin.site.register(Student) is no longer needed and should be removed if present.