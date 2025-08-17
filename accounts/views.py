

# --- 'redirect' IS NOW INCLUDED IN THIS IMPORT ---
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import CustomUserForm

def logout_view(request):
    """
    Logs the user out and redirects them to the login page.
    """
    logout(request)
    return redirect('accounts:login')


def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:add_user')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/add_user.html', {'form': form})