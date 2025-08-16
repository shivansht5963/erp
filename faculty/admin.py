from django.contrib import admin

from django.contrib import admin

from faculty.forms import TeacherWithUserForm
from .models import Notification
from .models import Department, Course, Class, Teacher, Subject

# faculty/admin.py
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherWithUserForm
    list_display = (
        'user', 'department',
        'qualification', 'contact_number', 'join_date'
    )
    search_fields = (
        'user__username', 'user__email', 'department__name'
    )

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Subject)
admin.site.register(Notification)
