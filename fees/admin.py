
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from students.models import Student
from django.contrib import messages
from django.http import HttpResponseRedirect

# Proxy model for Student to show in FeeReminder context
class StudentFeeStatus(Student):
    """Proxy model to manage student fee status and reminders in admin"""
    class Meta:
        proxy = True
        verbose_name = 'Student Fee Status'
        verbose_name_plural = 'Student Fee Status'


@admin.register(StudentFeeStatus)
class StudentFeeStatusAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'student_name', 'fee_status', 'amount_due', 'next_due_date', 'reminder_actions')
    list_filter = ('course', 'semester')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')
    actions = ['send_fee_reminders']

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:student_id>/remind/', 
                self.admin_site.admin_view(self.send_reminder), 
                name='student_send_reminder'),
        ]
        return custom_urls + urls

    def student_name(self, obj):
        return f"{obj.user.get_full_name()}"
    student_name.short_description = 'Student Name'

    def fee_status(self, obj):
        from fees.models import FeePayment
        summary = FeePayment.get_student_fee_summary(obj)
        status = summary['fee_status']
        if status == 'paid':
            return format_html('<span style="color: green;">{}</span>', '✓ Paid')
        elif status == 'partial':
            return format_html('<span style="color: orange;">{}</span>', '⚠ Partially Paid')
        return format_html('<span style="color: red;">{}</span>', '✗ Unpaid')
    fee_status.short_description = 'Payment Status'

    def amount_due(self, obj):
        from fees.models import FeePayment
        summary = FeePayment.get_student_fee_summary(obj)
        amount = summary['amount_due']
        if amount > 0:
            amount_str = '₹{:,.2f}'.format(amount)
            return format_html('<span style="color: red;">{}</span>', amount_str)
        return format_html('<span style="color: green;">{}</span>', '₹0.00')
    amount_due.short_description = 'Amount Due'

    def next_due_date(self, obj):
        from fees.models import FeePayment
        summary = FeePayment.get_student_fee_summary(obj)
        due_date = summary.get('next_due_date')
        if due_date:
            if due_date < timezone.now().date():
                return format_html('<span style="color: red;">{}</span>', due_date)
            return due_date
        return '-'
    next_due_date.short_description = 'Next Due Date'

    def reminder_actions(self, obj):
        from fees.models import FeeReminder
        if FeeReminder.objects.filter(student=obj, sent=False).exists():
            return format_html(
                '<span style="color: orange;">Reminder Pending</span>'
            )
        remind_url = reverse('admin:student_send_reminder', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Send Reminder</a>', 
            remind_url
        )
    reminder_actions.short_description = 'Actions'

    def send_reminder(self, request, student_id):
        from fees.models import FeeReminder, FeePayment
        student = Student.objects.get(pk=student_id)
        summary = FeePayment.get_student_fee_summary(student)
        
        if summary['amount_due'] <= 0:
            messages.warning(request, "No fees due for {}".format(student))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        amount_str = '₹{:,.2f}'.format(summary['amount_due'])
        full_name = student.user.get_full_name()
        due_date = summary.get('next_due_date', 'soon')
        
        reminder = FeeReminder.objects.create(
            student=student,
            reminder_date=timezone.now().date(),
            subject="Fee Payment Reminder - {} Due".format(amount_str),
            message="Dear {},\n\nThis is a reminder that you have {} in pending fees. "
                   "Please make the payment before {}.".format(full_name, amount_str, due_date),
            created_by=request.user,
            sent=False,  # This will make it show as a pop-up in the student dashboard
            amount_due=summary['amount_due'],
            due_date=summary.get('next_due_date') or timezone.now().date()
        )
        
        messages.success(request, f"Reminder created for {student}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def send_fee_reminders(self, request, queryset):
        from fees.models import FeeReminder, FeePayment
        reminders_created = 0
        
        for student in queryset:
            summary = FeePayment.get_student_fee_summary(student)
            if summary['amount_due'] > 0:
                amount_str = '₹{:,.2f}'.format(summary['amount_due'])
                full_name = student.user.get_full_name()
                due_date = summary.get('next_due_date', 'soon')
                
                FeeReminder.objects.create(
                    student=student,
                    reminder_date=timezone.now().date(),
                    subject="Fee Payment Reminder - {} Due".format(amount_str),
                    message="Dear {},\n\nThis is a reminder that you have {} in pending fees. "
                           "Please make the payment before {}.".format(full_name, amount_str, due_date),
                    created_by=request.user,
                    sent=False,
                    amount_due=summary['amount_due'],
                    due_date=summary.get('next_due_date') or timezone.now().date()
                )
                reminders_created += 1
        
        messages.success(request, "Created {} reminders for students with pending fees.".format(reminders_created))
    send_fee_reminders.short_description = "Send fee reminders to selected students"
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import FeeCategory, FeeStructure, FeePayment, FeeReminder, FeeCategoryAmount
from students.models import Student


class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'student_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('name',)

    def student_count(self, obj):
        return obj.get_students().count()
    student_count.short_description = 'Students'

    def get_students_display(self, obj):
        students = obj.get_students()
        if not students:
            return "No students"
        return ", ".join([f"{s.roll_number} - {s.user.get_full_name()}" for s in students])
    get_students_display.short_description = 'Students in Category'

    readonly_fields = ('created_at', 'get_students_display')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Students in Category', {
            'fields': ('get_students_display',)
        }),
        ('System Information', {
            'fields': ('created_at',)
        })
    )


class FeeCategoryAmountInline(admin.TabularInline):
    model = FeeCategoryAmount
    extra = len(FeeCategory.CATEGORY_CHOICES)  # Create an entry for each category
    min_num = len(FeeCategory.CATEGORY_CHOICES)  # Require all categories to be filled
    can_delete = False  # Don't allow deleting category amounts
    
    def get_queryset(self, request):
        # Only show existing amounts
        return super().get_queryset(request)
    
    def get_extra(self, request, obj=None, **kwargs):
        # If editing existing object, don't add extra forms
        if obj:
            return 0
        return len(FeeCategory.CATEGORY_CHOICES)

class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('course', 'academic_year', 'fee_type', 'amount', 'due_date', 'is_active')
    list_filter = ('is_active', 'academic_year', 'course')
    search_fields = ('academic_year', 'course__name', 'fee_type')
    list_editable = ('is_active',)
    ordering = ('-academic_year', 'course__name')
    inlines = [FeeCategoryAmountInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('course', 'academic_year', 'fee_type', 'is_active')
        }),
        ('Fee Information', {
            'fields': (
                'amount',
            ),
            'description': 'Base fee amount. Set category-specific amounts below.'
        }),
        ('Important Dates', {
            'fields': ('due_date',)
        }),
    )


class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_info', 'fee_structure_info', 'amount', 'payment_date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'payment_date', 'fee_structure__course')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__roll_number', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    date_hierarchy = 'payment_date'
    list_select_related = ('student__user', 'fee_structure__category', 'created_by')
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                ('student', 'fee_structure'),
                ('amount', 'payment_date'),
                ('payment_method', 'transaction_id'),
                'remarks'
            )
        }),
        ('System Information', {
            'classes': ('collapse',),
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def student_info(self, obj):
        url = reverse('admin:students_student_change', args=[obj.student.id])
        return format_html('<a href="{}">{} ({})</a>', url, obj.student, obj.student.roll_number)
    student_info.short_description = 'Student'
    
    def fee_structure_info(self, obj):
        return f"{obj.fee_structure.course.name} - {obj.fee_structure.academic_year}"
    fee_structure_info.short_description = 'Fee Structure'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student__user', 'fee_structure__course')


class FeeReminderAdmin(admin.ModelAdmin):
    list_display = ('student_info', 'subject', 'reminder_date', 'notification_status', 'sent_date', 'created_by')
    list_filter = ('sent', 'reminder_date', 'created_by')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__roll_number', 'subject', 'message')
    readonly_fields = ('sent', 'sent_date', 'created_by', 'created_at')
    ordering = ('-reminder_date', '-created_at')
    
    fieldsets = (
        ('Reminder Information', {
            'fields': (
                'student',
                ('subject', 'reminder_date'),
                'message',
            )
        }),
        ('Notification Status', {
            'fields': (
                ('sent', 'sent_date'),
            )
        }),
        ('System Information', {
            'classes': ('collapse',),
            'fields': (
                'created_by',
                'created_at',
            )
        }),
    )
    
    def student_info(self, obj):
        url = reverse('admin:students_student_change', args=[obj.student.id])
        name = obj.student.user.get_full_name() or obj.student.roll_number
        return format_html(
            '<a href="{}">{} ({})</a>', 
            url, 
            name, 
            obj.student.roll_number
        )
    student_info.short_description = 'Student'
    
    def notification_status(self, obj):
        if obj.sent:
            return format_html('<span style="color: green;">✓ Notified</span>')
        else:
            return format_html('<span style="color: orange;">⚠ Pending</span>')
    notification_status.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        """Only allow creating reminders through the Student Fee Status view"""
        return False


# Register the admin classes
admin.site.register(FeeCategory, FeeCategoryAdmin)
admin.site.register(FeeStructure, FeeStructureAdmin)
admin.site.register(FeePayment, FeePaymentAdmin)
admin.site.register(FeeReminder, FeeReminderAdmin)

# Note: StudentFeeStatus is registered using the @admin.register decorator above
