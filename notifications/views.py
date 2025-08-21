from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import TeacherNotificationForm
from faculty.models import Teacher
from students.models import Student
from .models import Notification

@login_required
@login_required
def check_new_notifications(request):
    """Check for new notifications and return them as JSON."""
    if not hasattr(request.user, 'student'):
        return JsonResponse({'error': 'User is not a student'}, status=403)
        
    notifications = Notification.objects.filter(
        recipient=request.user.student,
        is_read=False
    ).order_by('-created_at')[:5]
    
    notifications_html = render_to_string(
        'notifications/notification_list.html',
        {'notifications': notifications}
    )
    
    return JsonResponse({
        'count': notifications.count(),
        'notifications_html': notifications_html
    })

@login_required
@require_POST
@csrf_exempt
def mark_all_read(request):
    """Mark all notifications as read for the current user."""
    if not hasattr(request.user, 'student'):
        return JsonResponse({'error': 'User is not a student'}, status=403)
        
    Notification.objects.filter(
        recipient=request.user.student,
        is_read=False
    ).update(
        is_read=True,
        read_at=timezone.now()
    )
    
    return JsonResponse({'status': 'ok'})

@login_required
def create_teacher_notification(request):
    # Ensure the user is a teacher
    try:
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home') # Redirect to a 'home' page if it exists

    if request.method == 'POST':
        form = TeacherNotificationForm(request.POST, teacher=teacher)
        if form.is_valid():
            target_class = form.cleaned_data['target_class']
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']

            # Find all students in the target class
            students_in_class = Student.objects.filter(
                course__department=target_class.department,
                semester=target_class.semester
            )

            # Create a notification for each student
            for student in students_in_class:
                Notification.objects.create(
                    sender=request.user,
                    recipient=student,
                    title=title,
                    message=message
                )

            messages.success(request, f"Announcement sent to {students_in_class.count()} students in {target_class}.")
            return redirect('notifications:create_teacher_notification')
    else:
        form = TeacherNotificationForm(teacher=teacher)
        
    return render(request, 'notifications/create_notification.html', {'form': form})

