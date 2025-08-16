from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, add_user

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('add/', add_user, name='add_user'),
]
