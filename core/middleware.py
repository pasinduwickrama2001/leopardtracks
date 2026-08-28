import os
from pathlib import Path
from django.core.management import call_command

_DB_INITIALIZED = False

class AutoDatabaseInitMiddleware:
    """
    Middleware that automatically initializes migrations and seeds initial database
    fixtures (packages, tours, blogs, reviews) on Vercel serverless cold-start,
    and sets high-performance SEO and security headers.
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

        # Performance & SEO Crawl Headers
        if not response.has_header('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        if not response.has_header('Referrer-Policy'):
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response
