from django.contrib import admin

from django.contrib import admin
from .models import Notification
from .models import Department, Course, Class, Teacher, Subject

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Notification)
