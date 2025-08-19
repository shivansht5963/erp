# File: accounts/admin.py
from django.contrib import admin
from .models import CustomUser, Notification
from .forms import NotificationAdminForm

class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    list_display = ('title', 'recipient', 'send_to_all_students', 'created_by', 'created_at')
    list_filter = ('created_at', 'send_to_all_students')
    fields = ('recipient', 'send_to_all_students', 'title', 'message', 'read')

    def save_model(self, request, obj, form, change):
        """Automatically set the creator to the current user."""
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Filters the list of notifications:
        - Superusers (admins) can see all notifications.
        - Other staff (teachers) can only see notifications they created.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def has_module_permission(self, request):
        """
        Show the "Notifications" link ONLY to admins and faculty.
        Students will not see this section.
        """
        return request.user.role in ['admin', 'faculty']

    def has_change_permission(self, request, obj=None):
        """
        Allow changing a notification ONLY if the user is the one who created it.
        Superusers can change anything.
        """
        if obj is not None and not request.user.is_superuser and obj.created_by != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        """
        Allow deleting a notification ONLY if the user is the one who created it.
        Superusers can delete anything.
        """
        if obj is not None and not request.user.is_superuser and obj.created_by != request.user:
            return False
        return True

# Register your models with the admin site
admin.site.register(CustomUser)
admin.site.register(Notification, NotificationAdmin)