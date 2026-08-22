import os
from pathlib import Path
from django.core.management import call_command

_DB_INITIALIZED = False

class AutoDatabaseInitMiddleware:
    """
    Middleware that automatically initializes migrations and seeds initial database
    fixtures (packages, tours, blogs, reviews) on Vercel serverless cold-start.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _DB_INITIALIZED

        if not _DB_INITIALIZED:
            try:
                from core.models import SafariPackage
                # Check if database has records
                if SafariPackage.objects.count() == 0:
                    call_command('migrate', interactive=False)
                    fixture = Path(__file__).resolve().parent.parent / 'initial_data.json'
                    if fixture.exists():
                        call_command('loaddata', str(fixture), interactive=False)
                _DB_INITIALIZED = True
            except Exception:
                try:
                    # Tables missing: create tables and seed initial fixture data
                    call_command('migrate', interactive=False)
                    fixture = Path(__file__).resolve().parent.parent / 'initial_data.json'
                    if fixture.exists():
                        call_command('loaddata', str(fixture), interactive=False)
                    _DB_INITIALIZED = True
                except Exception:
                    pass

        response = self.get_response(request)
        return response
