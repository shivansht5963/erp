from django.urls import path
from django.contrib.auth import views as auth_views

# CORRECTED IMPORT: We remove 'dashboard' and add 'student_dashboard'
from .views import add_user, dashboard

app_name = 'accounts'

urlpatterns = [
    # URLs for login and logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add/', add_user, name='add_user'),
    path('dashboard/', dashboard, name='dashboard'),
]