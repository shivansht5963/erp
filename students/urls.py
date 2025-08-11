# students/urls.py
from django.urls import path
from . import views
app_name ='students'
urlpatterns = [
    path('add/', views.add_student,name='add_student'),
    # path('',views.student_list, name='student_list'),
    # path('<int:pk>/edit', views.edit_student, name = 'edit_student'),
]