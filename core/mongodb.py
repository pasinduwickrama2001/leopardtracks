import os
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
_mongo_client = None

DEFAULT_MONGODB_NAME = 'leopardtracks_db'

class MongoPackageModel:
    def __init__(self, doc):
        self._doc = doc
        self.id = doc.get('id', 1)
        self.pk = self.id
        self.title = doc.get('title', '')
        self.subtitle = doc.get('subtitle', '')
        self.slug = doc.get('slug', '')
        self.imageUrl = doc.get('imageUrl', '') or '/static/images/yala-tent.jpg'
        self.image_file = None
        self.image_urls = doc.get('image_urls', '')
        self.description = doc.get('description', '')
        self.category = doc.get('category', 'half-day')
        self.category_label = doc.get('category_label', 'HALF-DAY GAME DRIVE')
        self.tag_class = doc.get('tag_class', 'tag-sage')
        self.price_type = doc.get('price_type', 'jeep_only')
        self.price = str(doc.get('price', '$55.00'))
        self.price_unit = doc.get('price_unit', 'per 4x4 jeep (up to 7 guests)')
        self.mealPrice = str(doc.get('mealPrice', '0'))
        self.ticketPrice = str(doc.get('ticketPrice', '46'))
        self.childTicketPrice = str(doc.get('childTicketPrice', '20'))
        self.includes_tickets = doc.get('includes_tickets', False)
        self.ticket_addon_price = doc.get('ticket_addon_price', '')
        self.includes_breakfast = doc.get('includes_breakfast', False)
        self.breakfast_addon_price = doc.get('breakfast_addon_price', '')
        self.duration = doc.get('duration', '4 Hours')
        self.vehicle = doc.get('vehicle', 'Private 4x4 Safari Jeep')
        self.inclusions = doc.get('inclusions', '')
        self.exclusions = doc.get('exclusions', '')
        self.highlights = doc.get('highlights', '')
        self.featured = doc.get('featured', False)

    def get_clean_price(self):
        return str(self.price).replace('$', '').strip()

    def get_inclusions_list(self):
        if not self.inclusions:
            return []
        return [inc.strip() for inc in str(self.inclusions).split('\n') if inc.strip()]

    def get_exclusions_list(self):
        if not self.exclusions:
            return []
        return [exc.strip() for exc in str(self.exclusions).split('\n') if exc.strip()]

    def get_highlights_list(self):
        if not self.highlights:
            return []
        return [hl.strip() for hl in str(self.highlights).split('\n') if hl.strip()]

    def get_image_urls_list(self):
        urls = [self.imageUrl] if self.imageUrl else []
        if self.image_urls:
            extra = [u.strip() for u in str(self.image_urls).split('\n') if u.strip()]
            urls.extend(extra)
        return urls


class MongoTourModel:
    def __init__(self, doc):
        self._doc = doc
        self.id = doc.get('id', 1)
        self.pk = self.id
        self.title = doc.get('title', '')
        self.slug = doc.get('slug', '')
        self.route = doc.get('route', '')
        self.price = str(doc.get('price', '280'))
        self.duration = doc.get('duration', '')
        self.imageUrl = doc.get('imageUrl', '') or '/static/images/yala-wildlife-hero.jpg'
        self.description = doc.get('description', '')
        self.longDescription = doc.get('longDescription', '') or self.description
        self.highlights = doc.get('highlights', '')
        self.inclusions = doc.get('inclusions', '')
        self.exclusions = doc.get('exclusions', '')
        self.itinerary_json = doc.get('itinerary_json', '')
        self.isFeatured = doc.get('isFeatured', True)

    def get_clean_price(self):
        return str(self.price).replace('$', '').strip()

    def get_tour_image_url(self):
        return self.imageUrl

    def get_highlights_list(self):
        if not self.highlights:
            return []
        return [h.strip() for h in str(self.highlights).split('\n') if h.strip()]

    def get_inclusions_list(self):
        if not self.inclusions:
            return []
        return [i.strip() for i in str(self.inclusions).split('\n') if i.strip()]

    def get_exclusions_list(self):
        if not self.exclusions:
            return []
        return [e.strip() for e in str(self.exclusions).split('\n') if e.strip()]

    def get_itinerary_list(self):
        if not self.itinerary_json:
            return []
        try:
            return json.loads(self.itinerary_json)
        except Exception:
            return []


class MongoBlogModel:
    def __init__(self, doc):
        self._doc = doc
        self.id = doc.get('id', 1)
        self.pk = self.id
        self.title = doc.get('title', '')
        self.slug = doc.get('slug', '')
        self.category = doc.get('category', 'WILDLIFE')
        self.author = doc.get('author', 'Senior Naturalist Desk')
        self.imageUrl = doc.get('imageUrl', '') or '/static/images/yala-wildlife-hero.jpg'
        self.content = doc.get('content', '')
        self.featured = doc.get('featured', False)
        self.created_at = doc.get('created_at', 'August 2026')

    def get_paragraphs(self):
        if not self.content:
            return []
        return [p.strip() for p in str(self.content).split('\n\n') if p.strip()]


class MongoHeroModel:
    def __init__(self, doc):
        self._doc = doc
        self.id = doc.get('id', 1)
        self.title = doc.get('title', 'Yala National Park Safaris')
        self.subtitle = doc.get('subtitle', 'Luxury Tented Camps & Expeditions')
        self.description = doc.get('description', '')
        self.bg_image_url = doc.get('bg_image_url', '') or doc.get('imageUrl', '')
        self.cta_text = doc.get('cta_text', 'Book Now')
        self.cta_link = doc.get('cta_link', '#plan-your-stay')
        self.is_active = doc.get('is_active', True)


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

def fetch_mongo_package_by_slug(slug):
    db = get_mongo_db()
    if db is None:
        return None
    try:
        doc = db.core_safaripackage.find_one({'slug': slug})
        if not doc and slug.isdigit():
            doc = db.core_safaripackage.find_one({'id': int(slug)})
        if not doc:
            doc = db.packages.find_one({'slug': slug})
        return MongoPackageModel(doc) if doc else None
    except Exception as e:
        logger.error(f"Error fetching package by slug {slug} from MongoDB: {e}")
        return None

def fetch_mongo_tours():
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_tour.find())
    except Exception as e:
        logger.error(f"Error fetching tours from MongoDB: {e}")
        return None

def fetch_mongo_tour_by_slug(slug):
    db = get_mongo_db()
    if db is None:
        return None
    try:
        doc = db.core_tour.find_one({'slug': slug})
        if not doc and slug.isdigit():
            doc = db.core_tour.find_one({'id': int(slug)})
        return MongoTourModel(doc) if doc else None
    except Exception as e:
        logger.error(f"Error fetching tour by slug {slug} from MongoDB: {e}")
        return None

def fetch_mongo_blogs():
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_blogpost.find())
    except Exception as e:
        logger.error(f"Error fetching blogs from MongoDB: {e}")
        return None

def fetch_mongo_blog_by_slug(slug):
    db = get_mongo_db()
    if db is None:
        return None
    try:
        doc = db.core_blogpost.find_one({'slug': slug})
        if not doc and slug.isdigit():
            doc = db.core_blogpost.find_one({'id': int(slug)})
        return MongoBlogModel(doc) if doc else None
    except Exception as e:
        logger.error(f"Error fetching blog by slug {slug} from MongoDB: {e}")
        return None

def fetch_mongo_reviews(limit=50):
    db = get_mongo_db()
    if db is None:
        return None
    try:
        return list(db.core_guestreview.find().limit(limit))
    except Exception as e:
        logger.error(f"Error fetching reviews from MongoDB: {e}")
        return None

def fetch_mongo_heroes():
    db = get_mongo_db()
    if db is None:
        return None
    try:
        docs = list(db.core_herosection.find())
        return [MongoHeroModel(d) for d in docs] if docs else None
    except Exception as e:
        logger.error(f"Error fetching hero sections from MongoDB: {e}")
        return None
