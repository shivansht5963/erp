# File: faculty/admin.py
from django.contrib import admin
from .models import Department, Course, Class, Teacher, Subject

# Original registrations for other faculty models
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)