from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # This is the configuration for the admin panel.
    model = CustomUser
    
    # These fields will be displayed in the list view of users
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    
    # These fields will be used for filtering users in the admin panel
    list_filter = ('role', 'is_staff', 'is_active')
    
    # These fields will be searchable
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # The order of fields in the edit/creation form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'role')}),
        ('Contact info', {'fields': ('phone', 'dob', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Unregister the default User model if it was registered, and register our custom one with the new admin class.
# Note: Since we use a custom user model from the start, we just need to register CustomUser.
admin.site.register(CustomUser, CustomUserAdmin)