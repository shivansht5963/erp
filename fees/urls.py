# fees/urls.py
from django.urls import path
from .views import add_fee_category, add_fee_structure, add_fee_payment, add_fee_reminder

app_name = 'fees'

urlpatterns = [
    path('add_fee_category/', add_fee_category, name='add_fee_category'),
    path('add_fee_structure/', add_fee_structure, name='add_fee_structure'),
    path('add_fee_payment/', add_fee_payment, name='add_fee_payment'),
    path('add_fee_reminder/', add_fee_reminder, name='add_fee_reminder'),
]