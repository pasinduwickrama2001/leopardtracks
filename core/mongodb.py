import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
_mongo_client = None

DEFAULT_MONGODB_URI = 'mongodb+srv://pasinduwickramasooriya_db_user:mynameispasindu@cluster0.uj70orq.mongodb.net/leopardtracks_db?retryWrites=true&w=majority'

def is_mongodb_active():
    """
    Check if MongoDB Atlas is enabled via environment variables or settings.
    """
    val = os.getenv('USE_MONGODB', '')
    if val:
        return val.lower() in ('true', '1', 'yes')
    return getattr(settings, 'USE_MONGODB', False)

def get_mongo_db():
    """
    Get active PyMongo database connection to MongoDB Atlas.
    """
    global _mongo_client
    try:
        import pymongo
        uri = os.getenv('MONGODB_URI', '') or getattr(settings, 'MONGODB_URI', '') or DEFAULT_MONGODB_URI
        db_name = os.getenv('MONGODB_NAME', '') or getattr(settings, 'MONGODB_NAME', 'leopardtracks_db') or 'leopardtracks_db'

        if _mongo_client is None:
            _mongo_client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        
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
