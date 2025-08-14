from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
    
    def ready(self):
        """
        This method is called when the app is ready.
        Importing the signals here ensures they are connected when Django starts.
        """
        import attendance.signals
