from django.apps import AppConfig

class CaseTrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "case_tracker"

    def ready(self):
        import case_tracker.signals  # Django 載入 signals.py
