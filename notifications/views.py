# notifications/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden

from .forms import NotificationForm
from .models import Notification, UserNotificationStatus
from students.models import Student
from accounts.models import CustomUser

def is_staff(user):
    return user.is_authenticated and user.role in ['admin', 'faculty']

@user_passes_test(is_staff)
def create_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            
            notification = Notification.objects.create(
                title=data['title'],
                message=data['message'],
                created_by=request.user
            )

            # Determine recipients
            recipients = []
            audience_type = data['audience_type']

            if audience_type == 'all_students':
                recipients = CustomUser.objects.filter(role='student')
            elif audience_type == 'class':
                target_class = data['target_class']
                students_in_class = Student.objects.filter(
                    course__department=target_class.department, 
                    semester=target_class.semester
                )
                recipients = [student.user for student in students_in_class]
            elif audience_type == 'student':
                target_student = data['target_student']
                recipients = [target_student.user]

            # Create UserNotificationStatus for each recipient
            for user in recipients:
                UserNotificationStatus.objects.create(user=user, notification=notification)

            messages.success(request, 'Notification sent successfully!')
            return redirect('notifications:create')
    else:
        form = NotificationForm(user=request.user)
        
    return render(request, 'notifications/create_notification.html', {'form': form})

@login_required
def notification_list(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")

    notifications = UserNotificationStatus.objects.filter(user=request.user).select_related('notification', 'notification__created_by').order_by('-notification__created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})


@login_required
def mark_notification_as_read(request, status_id):
    notification_status = get_object_or_404(UserNotificationStatus, id=status_id, user=request.user)
    notification_status.mark_as_read()
    messages.info(request, f'Notification "{notification_status.notification.title}" marked as read.')
    return redirect('notifications:list')