# File: accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_user, redirect_after_login, faculty_dashboard, student_dashboard

app_name = 'accounts'

urlpatterns = [
    # The login view remains the same
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # This URL is the target for LOGIN_REDIRECT_URL
    path('redirect/', redirect_after_login, name='login_redirect'),

    # Dashboard URLs (Admin dashboard URL removed)
    path('dashboard/faculty/', faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/student/', student_dashboard, name='student_dashboard'),

    # Your existing add_user URL
    path('add/', add_user, name='add_user'),
]