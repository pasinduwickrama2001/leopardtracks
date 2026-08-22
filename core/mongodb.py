import os
import logging

logger = logging.getLogger(__name__)
_mongo_client = None

DEFAULT_MONGODB_NAME = 'leopardtracks_db'

def get_mongo_uri():
    uri = os.getenv('MONGODB_URI', '').strip()
    if not uri:
        try:
            from django.conf import settings
            if getattr(settings, 'configured', False):
                uri = getattr(settings, 'MONGODB_URI', '').strip()
        except Exception:
            pass
    return uri

def get_mongo_dbname():
    name = os.getenv('MONGODB_NAME', '').strip()
    if not name:
        try:
            from django.conf import settings
            if getattr(settings, 'configured', False):
                name = getattr(settings, 'MONGODB_NAME', '').strip()
        except Exception:
            pass
    return name if name else DEFAULT_MONGODB_NAME

def is_mongodb_active():
    val = os.getenv('USE_MONGODB', '').strip()
    if val:
        return val.lower() in ('true', '1', 'yes')
    try:
        from django.conf import settings
        if getattr(settings, 'configured', False):
            return getattr(settings, 'USE_MONGODB', False)
    except Exception:
        pass
    return True

def get_mongo_db():
    global _mongo_client
    try:
        import pymongo
        uri = get_mongo_uri()
        if not uri:
            logger.warning("No MONGODB_URI found in environment variables.")
            return None

        db_name = get_mongo_dbname()

        if _mongo_client is None:
            _mongo_client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=8000)
        
        return _mongo_client[db_name]
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        return None


def fetch_mongo_packages():
    """
    Fetch all safari packages directly from MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        docs = list(db.core_safaripackage.find())
        if not docs:
            docs = list(db.packages.find())
        return docs
    except Exception as e:
        logger.error(f"Error fetching packages from MongoDB: {e}")
        return None

def fetch_mongo_tours():
    """
    Fetch all round tours directly from MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_tour.find())
    except Exception as e:
        logger.error(f"Error fetching tours from MongoDB: {e}")
        return None

def fetch_mongo_blogs():
    """
    Fetch all wildlife blogs directly from MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_blogpost.find())
    except Exception as e:
        logger.error(f"Error fetching blogs from MongoDB: {e}")
        return None

def fetch_mongo_reviews(limit=50):
    """
    Fetch guest reviews directly from MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_guestreview.find().limit(limit))
    except Exception as e:
        logger.error(f"Error fetching reviews from MongoDB: {e}")
        return None

def fetch_mongo_heroes():
    """
    Fetch hero banners directly from MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_herosection.find())
    except Exception as e:
        logger.error(f"Error fetching hero sections from MongoDB: {e}")
        return None
