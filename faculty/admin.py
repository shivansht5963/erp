# faculty/admin.py
from django.contrib import admin
from .models import Department, Course, Class, Teacher, Subject

class TeacherAdmin(admin.ModelAdmin):
    # Use filter_horizontal for a better ManyToMany widget in the admin
    filter_horizontal = ('departments',)
    list_display = ('user', 'get_departments', 'qualification')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    @admin.display(description='Departments')
    def get_departments(self, obj):
        return ", ".join([d.name for d in obj.departments.all()])

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Subject)
# Register the Teacher model with its custom admin class
admin.site.register(Teacher, TeacherAdmin)