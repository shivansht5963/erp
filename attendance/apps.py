# attendance/apps.py

from django.apps import AppConfig

class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    # This 'ready' method is how Django discovers your signals
    def ready(self):
        import attendance.signals