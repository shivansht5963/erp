from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TeacherNotificationForm
from faculty.models import Teacher
from students.models import Student
from .models import Notification

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

