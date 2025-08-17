from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_user, logout_view

# --- ADD THIS LINE ---
app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', add_user, name='add_user'),
]