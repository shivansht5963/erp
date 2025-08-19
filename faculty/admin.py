from django import forms
from django.contrib import admin
from django.db.models import Q
from .models import Department, Course, Class, Teacher, Subject, Announcement

# --- Step 1: Custom Form Field to Change Dropdown Labels ---

class ClassSubjectChoiceField(forms.ModelChoiceField):
    """
    A custom dropdown field that modifies the display label for each class
    to include the relevant subject(s) taught by the teacher.
    """
    def __init__(self, teacher, *args, **kwargs):
        self.teacher = teacher
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        # 'obj' is a Class instance from the queryset.
        # Find the subject(s) this teacher teaches for this specific class.
        subjects = Subject.objects.filter(
            teacher=self.teacher,
            department=obj.department,
            semester=obj.semester
        )
        subject_names = ", ".join([s.name for s in subjects])
        
        # Return the final, descriptive label.
        return f"{obj} (Subjects: {subject_names})"


# --- Step 2: The Final, Corrected AnnouncementAdmin Class ---

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    Final, robust admin configuration for Announcements using the correct Django hooks.
    """
    # Hide the 'teacher' field, which is set automatically.
    exclude = ('teacher',)
    list_display = ('title', 'teacher', 'target_class', 'created_at')
    list_filter = ('teacher', 'target_class')
    search_fields = ('title', 'message', 'teacher__user__first_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        This is the correct hook to customize the form field for 'target_class'.
        It filters the queryset AND applies the custom field with custom labels.
        """
        if db_field.name == "target_class" and not request.user.is_superuser:
            try:
                teacher = Teacher.objects.get(user=request.user)
                
                # --- Filter logic to find classes the teacher teaches in ---
                teacher_subject_details = Subject.objects.filter(teacher=teacher)\
                                                     .values_list('department_id', 'semester')\
                                                     .distinct()
                query = Q()
                for dept_id, sem in teacher_subject_details:
                    query |= Q(department_id=dept_id, semester=sem)

                class_queryset = Class.objects.filter(query) if query else Class.objects.none()
                
                # --- Return our custom field with the filtered queryset ---
                return ClassSubjectChoiceField(
                    teacher=teacher,
                    queryset=class_queryset,
                    label="Target Class & Subject"
                )
            except Teacher.DoesNotExist:
                # If user has no Teacher profile, show an empty dropdown.
                kwargs['queryset'] = Class.objects.none()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # --- PERMISSION CONTROLS (Unchanged) ---

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher__user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None: return True
        return obj.teacher.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None: return True
        return obj.teacher.user == request.user or request.user.is_superuser

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.teacher = Teacher.objects.get(user=request.user)
        super().save_model(request, obj, form, change)


# --- Register the other models ---
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)