# erp/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # <-- ADDED THIS IMPORT

def index(request):
    """
    This view renders your public-facing landing page.
    """
    return render(request, 'index.html')

# --- ADDED THE ENTIRE VIEW FUNCTION BELOW ---
@login_required
def home(request):
    """
    This view is the target for LOGIN_REDIRECT_URL.
    It will only be accessible to logged-in users.
    """
    return render(request, 'home.html')