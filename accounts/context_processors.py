# File: accounts/context_processors.py

from .models import Notification

def notifications(request):
    """
    Provides notification data to all templates for the logged-in user.
    """
    if request.user.is_authenticated:
        # --- START OF THE FIX ---
        # The field name was changed from 'user' to 'recipient'.
        # This line is now corrected.
        unread_notifications = Notification.objects.filter(recipient=request.user, read=False)
        # --- END OF THE FIX ---
        
        return {
            'notifications': unread_notifications,
            'unread_notifications_count': unread_notifications.count()
        }
    return {}