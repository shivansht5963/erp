# attendance/apps.py
from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    # --- Start of New Code ---
    def ready(self):
        import attendance.signals
    # --- End of New Code ---