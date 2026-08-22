from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import sys
        if any(cmd in sys.argv for cmd in ['collectstatic', 'makemigrations', 'dumpdata', 'help']):
            return

        try:
            from pathlib import Path
            from django.core.management import call_command
            from core.models import SafariPackage

            if SafariPackage.objects.count() == 0:
                fixture_file = Path(__file__).resolve().parent.parent / 'initial_data.json'
                if fixture_file.exists():
                    call_command('loaddata', str(fixture_file), interactive=False)
        except Exception:
            pass

