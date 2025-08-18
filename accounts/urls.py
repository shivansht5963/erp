# accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_user, dashboard, student_dashboard

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Redirect to the homepage after logging out
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('add/', add_user, name='add_user'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),
]