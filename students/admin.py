from django.contrib import admin

from students.forms import StudentWithUserForm
from .models import Student
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    form = StudentWithUserForm

    list_display = ('user', 'roll_number', 'course', 'semester')
    search_fields = ('roll_number', 'user__username', 'user__email')

admin.site.register(Student,StudentAdmin)