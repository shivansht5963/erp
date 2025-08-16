from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'faculty':
            return reverse_lazy('faculty:teacher_dashboard')
        elif user.role == 'student':
            return reverse_lazy('students:student_dashboard')
        return super().get_success_url()