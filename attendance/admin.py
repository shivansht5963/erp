# attendance/admin.py

from django.contrib import admin
from .models import Attendance, AttendanceReport
from faculty.models import Subject, Teacher
from students.models import Student

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Updated to show the new numeric fields instead of the old 'status'
    list_display = ('student', 'subject', 'date', 'classes_held', 'classes_attended', 'marked_by')
    # Updated to remove 'status' from the filters
    list_filter = ('subject', 'date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            teacher = request.user.teacher
            return qs.filter(subject__teacher=teacher)
        except (Teacher.DoesNotExist, AttributeError):
            return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            try:
                teacher = request.user.teacher
                if db_field.name == "subject":
                    kwargs["queryset"] = Subject.objects.filter(teacher=teacher)
                if db_field.name == "student":
                    taught_course_ids = Subject.objects.filter(teacher=teacher).values_list('course_id', flat=True).distinct()
                    kwargs["queryset"] = Student.objects.filter(course_id__in=taught_course_ids)
            except (Teacher.DoesNotExist, AttributeError):
                pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ['marked_by']

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'teacher'):
            obj.marked_by = request.user.teacher
        super().save_model(request, obj, form, change)


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'total_classes', 'classes_attended', 'attendance_percentage')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            teacher = request.user.teacher
            return qs.filter(subject__teacher=teacher)
        except (Teacher.DoesNotExist, AttributeError):
            return qs.none()