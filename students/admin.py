from django.contrib import admin
from .models import Student

# Create a custom admin class to improve the display
class StudentAdmin(admin.ModelAdmin):
    # 'list_display' controls which columns are shown in the admin list
    list_display = ('roll_number', 'get_full_name', 'course', 'semester', 'class_enrolled')
    
    # 'search_fields' adds a search bar to search by these fields
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')
    
    # 'list_filter' adds a sidebar to filter results
    list_filter = ('course', 'semester', 'class_enrolled')

    # This is a custom method to get the name from the related user model
    @admin.display(description='Full Name', ordering='user__first_name')
    def get_full_name(self, obj):
        return obj.user.get_full_name()

# Register the Student model with its custom admin options
admin.site.register(Student, StudentAdmin)