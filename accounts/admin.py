# accounts/admin.py
from django.contrib import admin
from .models import CustomUser,Notification # Import Notification

admin.site.register(CustomUser)
admin.site.register(Notification) # Register the Notification model