import os
import logging
from pathlib import Path
from django.core.management import call_command

logger = logging.getLogger(__name__)
_DB_INITIALIZED = False
_LAST_ADMIN_SYNC = 0

class AutoDatabaseInitMiddleware:
    """
    Middleware that automatically initializes migrations, ensures admin superuser,
    and syncs live records from MongoDB Atlas on Vercel serverless cold-start,
    and sets high-performance SEO and security headers.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _DB_INITIALIZED

        if not _DB_INITIALIZED:
            _DB_INITIALIZED = True
            try:
                # 1. Run migrations if tables are not yet created in /tmp/db.sqlite3
                try:
                    from core.models import SafariPackage
                    _ = SafariPackage.objects.count()
                except Exception:
                    call_command('migrate', interactive=False)

                # 2. Ensure Admin Superuser Exists
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    admin_user = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
                    admin_pass = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
                    admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@discoveryala.com')

                    user_obj = User.objects.filter(username=admin_user).first()
                    if not user_obj:
                        User.objects.create_superuser(
                            username=admin_user,
                            email=admin_email,
                            password=admin_pass
                        )
                    else:
                        if not user_obj.is_staff or not user_obj.is_superuser:
                            user_obj.is_staff = True
                            user_obj.is_superuser = True
                            user_obj.save()
                except Exception as e:

                    logger.warning(f"Superuser auto-check notice: {e}")

                # 3. Hydrate SQLite from live MongoDB Atlas
                try:
                    from core.mongodb import sync_all_from_mongo_to_sqlite, sync_all_from_sqlite_to_mongo
                    hydrated = sync_all_from_mongo_to_sqlite()
                    
                    # If database is completely empty (no packages), load initial fixture
                    from core.models import SafariPackage
                    if SafariPackage.objects.count() == 0:
                        fixture = Path(__file__).resolve().parent.parent / 'initial_data.json'
                        if fixture.exists():
                            call_command('loaddata', str(fixture), interactive=False)
                except Exception as e:
                    logger.warning(f"MongoDB hydration notice: {e}")

            except Exception as e:
                logger.error(f"AutoDatabaseInit error: {e}")

        # In Admin panel, ensure SQLite periodically has fresh MongoDB records (at most once every 5 minutes)
        global _LAST_ADMIN_SYNC
        import time
        now = time.time()
        if request.path == '/admin/' and getattr(request, 'user', None) and request.user.is_authenticated and request.user.is_staff:
            if now - _LAST_ADMIN_SYNC > 300:
                _LAST_ADMIN_SYNC = now
                try:
                    from core.mongodb import sync_all_from_mongo_to_sqlite
                    sync_all_from_mongo_to_sqlite()
                except Exception:
                    pass

        response = self.get_response(request)

        # Performance & SEO Crawl Headers
        if not response.has_header('X-Content-Type-Options'):
            response['X-Content-Type-Options'] = 'nosniff'
        if not response.has_header('Referrer-Policy'):
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response


