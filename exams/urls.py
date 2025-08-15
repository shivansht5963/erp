# exams/urls.py
app_name = 'exams'
from django.urls import path
from .views import add_subject, add_marks, update_marks

urlpatterns = [
    path('add_subject/', add_subject, name='add_subject'),
    path('add_marks/', add_marks, name='add_marks'),
    path('update_marks/<int:pk>/', update_marks, name='update_marks'),
]