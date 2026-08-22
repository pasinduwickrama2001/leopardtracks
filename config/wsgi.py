"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# Auto-run database migrations & seed initial data on serverless cold-start
try:
    from django.core.management import call_command
    from core.models import SafariPackage

    call_command('migrate', interactive=False)

    if SafariPackage.objects.count() == 0:
        fixture_path = Path(__file__).resolve().parent.parent / 'initial_data.json'
        if fixture_path.exists():
            call_command('loaddata', str(fixture_path), interactive=False)
except Exception:
    pass

app = application



