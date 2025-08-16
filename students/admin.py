from django.contrib import admin
from django.contrib import messages
from students.forms import StudentWithUserForm
from .models import Student
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    form = StudentWithUserForm

    list_display = ('user', 'roll_number', 'course', 'semester')
    search_fields = ('roll_number', 'user__username', 'user__email')
    
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        password = getattr(form, '_saved_password', None)
        if password:
            messages.success(request, f"User created! Password: {password} (copy now, it won't be shown again)")

admin.site.register(Student,StudentAdmin)