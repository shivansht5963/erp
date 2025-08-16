from django.contrib import admin
from .models import Student

# This file's only job is to register the Student model
# so it appears in the Django admin interface.
# It does not need to know about any forms.

admin.site.register(Student)