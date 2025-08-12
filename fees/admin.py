
from django.contrib import admin
from .models import FeeCategory, FeeStructure, FeePayment, FeeReminder

admin.site.register(FeeCategory)
admin.site.register(FeeStructure)
admin.site.register(FeePayment)
admin.site.register(FeeReminder)
