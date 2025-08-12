from django.shortcuts import render, redirect
from .forms import CustomUserForm

def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})
