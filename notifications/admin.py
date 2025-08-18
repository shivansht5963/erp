from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.utils.html import format_html

from .models import Notification
from .forms import AdminNotificationForm
from students.models import Student
from faculty.models import Class

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # This section is for DISPLAYING sent notifications
    list_display = ('recipient', 'title', 'sender', 'created_at', 'is_read')
    list_filter = ('is_read', 'sender', 'created_at')
    search_fields = ('title', 'recipient__user__username', 'sender__username')
    
    # We disable the default "Add" button because we have a custom one
    def has_add_permission(self, request):
        return False

    # This is the standard Django way to add custom URLs to an admin page
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send-announcement/',
                self.admin_site.admin_view(self.send_announcement_view),
                name='notifications_notification_send_announcement',
            ),
        ]
        return custom_urls + urls

    # This is our custom view that will live inside the admin
    def send_announcement_view(self, request):
        if request.method == 'POST':
            form = AdminNotificationForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                message = form.cleaned_data['message']
                target_type = form.cleaned_data['target_type']
                
                students_to_notify = []

                if target_type == 'all_students':
                    students_to_notify = Student.objects.all()
                elif target_type == 'class':
                    target_class = form.cleaned_data['target_class']
                    students_to_notify = Student.objects.filter(
                        course__department=target_class.department, 
                        semester=target_class.semester
                    )
                elif target_type == 'student':
                    student = form.cleaned_data['target_student']
                    if student:
                        students_to_notify = [student]

                # Create a notification for each student
                for student in students_to_notify:
                    Notification.objects.create(
                        sender=request.user,
                        recipient=student,
                        title=title,
                        message=message
                    )
                
                self.message_user(request, f'Notification sent to {len(students_to_notify)} student(s).', messages.SUCCESS)
                # Redirect back to the main notification list page
                return redirect('admin:notifications_notification_changelist')
        else:
            form = AdminNotificationForm()

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = 'Send Announcement'
        return render(request, 'admin/notifications/send_announcement.html', context)

    # We override the changelist_view to add a "Send Announcement" button
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Create the URL for our custom view
        url = reverse('admin:notifications_notification_send_announcement')
        # Add a button that links to our custom view
        extra_context['send_button'] = format_html(
            '<a href="{}" class="button">Send Announcement</a>', url
        )
        # We must explicitly tell Django to use our custom template
        self.change_list_template = 'admin/notifications/notification/change_list.html'
        return super().changelist_view(request, extra_context=extra_context)