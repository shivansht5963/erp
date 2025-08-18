from django.contrib.auth.decorators import user_passes_test

def is_faculty(user):
    """
    A decorator check to ensure a user is authenticated and has the 'faculty' role.
    """
    return user.is_authenticated and user.role == 'faculty'

def faculty_required(view_func):
    """
    Decorator for views that checks that the user is a faculty member,
    redirecting to the login page if necessary.
    """
    decorated_view_func = user_passes_test(is_faculty, login_url='/accounts/login/')
    return decorated_view_func(view_func)

# You can add more checks here later, like is_student, is_admin, etc.