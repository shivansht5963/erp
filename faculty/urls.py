from django.urls import path
from . import views
# from .views import add_department, add_course, add_class, add_teacher, teacher_dashboard
from .views import teacher_dashboard
app_name = 'faculty'

urlpatterns = [
    path('register/', views.register_teacher, name='register_teacher'),
    # path('add_department/', add_department, name='add_department'),
    # path('add_course/', add_course, name='add_course'),
    # path('add_class/', add_class, name='add_class'),
    # path('add_teacher/', add_teacher, name='add_teacher'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),

]
