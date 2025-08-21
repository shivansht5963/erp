from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import StudentForm, CustomUserCreationForm
from .models import Student
from exams.models import Marks
from fees.models import FeePayment, FeeReminder
from notifications.models import Notification
import json
@login_required
@csrf_exempt
def dismiss_fee_reminder(request):
    """
    View to handle dismissing fee reminders.
    """
    if request.method == 'POST':
        try:
            from django.utils import timezone
            from fees.models import FeeReminder
            
            student = request.user.student
            
            # Get all unread reminders for the student
            reminders = FeeReminder.objects.filter(
                student=student,
                sent=False
            )
            
            if reminders.exists():
                current_time = timezone.now()
                # Mark all unread reminders as sent
                reminders.update(sent=True, sent_date=current_time)
                return JsonResponse({
                    'status': 'ok',
                    'message': 'Fee reminders dismissed successfully'
                })
            return JsonResponse({
                'status': 'no_reminder',
                'message': 'No pending reminders found'
            })
            
        except Exception as e:
            import traceback
            print('Error in dismiss_fee_reminder:', str(e))
            print(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while dismissing the reminder'
            }, status=500)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)
# students/views.py
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.shortcuts import render, redirect
# from .forms import StudentForm
# from .models import Student
# import json

User = get_user_model()

# @user_passes_test(lambda u: u.is_staff)
def add_student(request):
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'student'
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "Student added successfully.")
            return redirect('students:add_student')
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()
    return render(request, 'students/add_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })


@login_required
def student_dashboard(request):
    """
    Displays the dashboard for the logged-in student, including personal details,
    attendance reports, and a pie chart of attendance percentages.
    """
    try:
        student = request.user.student
    except Student.DoesNotExist:
        # Handle cases where the user is not a student (e.g., faculty, admin)
        # You can redirect them to an appropriate page or show an error.
        messages.error(request, "You do not have a student profile.")
        return redirect('accounts:login') # Or your home page

    attendance_reports = student.view_attendance()

    # Prepare data for the Chart.js pie chart
    chart_labels = [report.subject.name for report in attendance_reports]
    chart_data = [report.attendance_percentage for report in attendance_reports]
    from exams.models import Marks
    marks = Marks.objects.filter(student=student).select_related('subject')

    # Get fee summary for the student
    from fees.models import FeePayment
    fee_summary = FeePayment.get_student_fee_summary(student)

    # Check for unsent fee reminder
    from fees.models import FeeReminder
    fee_reminder_popup = FeeReminder.objects.filter(student=student, sent=False).order_by('-reminder_date').first()

    context = {
        'student': student,
        'attendance_reports': attendance_reports,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'marks': marks,
        'fee_summary': fee_summary,
        'fee_reminder_popup': fee_reminder_popup,
    }
    # Get recent announcements
    from notifications.models import Notification
    notifications = Notification.objects.filter(
        recipient=student,
        is_read=False
    ).order_by('-created_at')[:5]
    
    # Add notifications to context
    context['notifications'] = notifications
    
    return render(request, 'students/dashboard.html', context)