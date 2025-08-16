from django.contrib import admin
from .models import Department, Course, Class, Teacher, Subject

# This file's only job is to register models with the Django admin site.
# It should not import forms.

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)