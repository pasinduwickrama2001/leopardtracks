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
        self.pk = self.id
        self.title = doc.get('title', 'WILD YALA SAFARIS')
        self.subtitle = doc.get('subtitle', "Ceylon's premier 4x4 game drives & luxury glamping.")
        self.description = doc.get('description', '')
        self.badge_text = doc.get('badge_text', 'YALA LEOPARD TRACKS')
        self.imageUrl = doc.get('imageUrl', '') or doc.get('bg_image_url', '') or '/static/images/yala-wildlife-hero.jpg'
        self.bg_image_url = self.imageUrl
        btn_p = doc.get('button_primary_text', 'PACKAGES')
        if btn_p == 'EXPLORE PACKAGES':
            btn_p = 'PACKAGES'
        self.button_primary_text = btn_p
        self.button_primary_url = doc.get('button_primary_url', '/packages/')

        btn_s = doc.get('button_secondary_text', 'BOOK SAFARI')
        if btn_s == 'RESERVE YALA SAFARI JEEP':
            btn_s = 'BOOK SAFARI'
        self.button_secondary_text = btn_s
        self.button_secondary_url = doc.get('button_secondary_url', '/contact/')

        self.cta_text = doc.get('cta_text', 'Book Now')
        self.cta_link = doc.get('cta_link', '#plan-your-stay')
        self.is_active = doc.get('is_active', True)

    def get_hero_image_url(self):
        if self.imageUrl and str(self.imageUrl).strip():
            return str(self.imageUrl).strip()
        return '/static/images/yala-wildlife-hero.jpg'


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

# ==============================================================================
# Model Serialization for MongoDB
# ==============================================================================

def package_to_dict(pkg):
    return {
        'id': pkg.id,
        'title': pkg.title or '',
        'subtitle': pkg.subtitle or '',
        'slug': pkg.slug or '',
        'imageUrl': pkg.imageUrl or '',
        'image_urls': pkg.image_urls or '',
        'description': pkg.description or '',
        'category': pkg.category or 'half-day',
        'category_label': pkg.category_label or 'HALF-DAY GAME DRIVE',
        'tag_class': pkg.tag_class or 'tag-sage',
        'price_type': pkg.price_type or 'jeep_only',
        'price': str(pkg.price or '$120'),
        'price_unit': pkg.price_unit or 'per 4x4 jeep (up to 6 guests)',
        'mealPrice': str(pkg.mealPrice or '0'),
        'ticketPrice': str(pkg.ticketPrice or '0'),
        'childTicketPrice': str(pkg.childTicketPrice or '20'),
        'includes_tickets': bool(pkg.includes_tickets),
        'ticket_addon_price': pkg.ticket_addon_price or '',
        'includes_breakfast': bool(pkg.includes_breakfast),
        'breakfast_addon_price': pkg.breakfast_addon_price or '',
        'duration': pkg.duration or '5 Hours (05:30 AM – 10:30 AM)',
        'vehicle': pkg.vehicle or 'Private Modified Toyota Land Cruiser 4x4',
        'inclusions': pkg.inclusions or '',
        'exclusions': pkg.exclusions or '',
        'highlights': pkg.highlights or '',
        'featured': bool(pkg.featured),
    }

def tour_to_dict(tour):
    return {
        'id': tour.id,
        'title': tour.title or '',
        'slug': tour.slug or '',
        'route': tour.route or '',
        'price': str(tour.price or '280'),
        'duration': tour.duration or '5 Days / 4 Nights',
        'imageUrl': tour.imageUrl or '',
        'isFeatured': bool(tour.isFeatured),
        'description': tour.description or '',
        'longDescription': tour.longDescription or '',
        'highlights': tour.highlights or '',
        'inclusions': tour.inclusions or '',
        'exclusions': tour.exclusions or '',
        'seoKeywords': tour.seoKeywords or '',
        'itinerary_json': tour.itinerary_json or '',
    }

def blog_to_dict(blog):
    return {
        'id': blog.id,
        'title': blog.title or '',
        'slug': blog.slug or '',
        'category': blog.category or 'WILDLIFE LOG',
        'author': blog.author or 'Discoveryala Naturalist',
        'imageUrl': blog.imageUrl or '',
        'content': blog.content or '',
        'featured': bool(blog.featured),
    }

def hero_to_dict(hero):
    return {
        'id': hero.id,
        'title': hero.title or 'WILD YALA SAFARIS',
        'subtitle': hero.subtitle or "Ceylon's premier 4x4 game drives & luxury glamping.",
        'badge_text': hero.badge_text or '🌿 YALA LEOPARD TRACKS',
        'imageUrl': hero.imageUrl or '',
        'button_primary_text': hero.button_primary_text or 'EXPLORE PACKAGES',
        'button_primary_url': hero.button_primary_url or '/packages/',
        'button_secondary_text': hero.button_secondary_text or 'BOOK SAFARI',
        'button_secondary_url': hero.button_secondary_url or '/contact/',
        'is_active': bool(hero.is_active),
    }

def review_to_dict(rev):
    return {
        'id': rev.id,
        'category': rev.category or 'leopard',
        'name': rev.name or '',
        'origin': rev.origin or 'London, UK',
        'date': rev.date or 'August 2026',
        'package': rev.package or 'Yala Block 1 Morning Leopard Game Drive',
        'rating': int(rev.rating or 5),
        'comment': rev.comment or '',
        'verified': bool(rev.verified),
        'avatar_url': rev.avatar_url or '',
        'photo_url': rev.photo_url or '',
        'source': rev.source or 'Google Maps',
    }

def booking_to_dict(b):
    return {
        'id': b.id,
        'package_title': b.package_title or '',
        'full_name': b.full_name or '',
        'country': b.country or '',
        'email': b.email or '',
        'phone_code': b.phone_code or '+94',
        'phone_number': b.phone_number or '',
        'safari_date': str(b.safari_date) if b.safari_date else '',
        'guests': int(b.guests or 2),
        'adult_guests': int(b.adult_guests or 2),
        'child_guests': int(b.child_guests or 0),
        'under6_guests': int(b.under6_guests or 0),
        'include_meals': bool(b.include_meals),
        'meal_count': int(b.meal_count or 0),
        'meals_price_total': str(b.meals_price_total or '0'),
        'include_tickets': bool(b.include_tickets),
        'tickets_price_total': str(b.tickets_price_total or '0'),
        'base_price': str(b.base_price or '0'),
        'total_price': str(b.total_price or '0'),
        'message': b.message or '',
        'status': b.status or 'Pending',
    }

# ==============================================================================
# Real-Time MongoDB CRUD Operations (Triggered on Django Admin actions)
# ==============================================================================

def sync_model_to_mongo(instance):
    """
    Called whenever an instance is created or updated in Django Admin.
    Upserts the corresponding document in MongoDB Atlas in real time.
    """
    db = get_mongo_db()
    if db is None:
        return False
    try:
        model_name = instance.__class__.__name__
        if model_name == 'SafariPackage':
            doc = package_to_dict(instance)
            filter_query = {'slug': instance.slug} if instance.slug else {'id': instance.id}
            db.core_safaripackage.replace_one(filter_query, doc, upsert=True)
            db.packages.replace_one(filter_query, doc, upsert=True)
        elif model_name == 'Tour':
            doc = tour_to_dict(instance)
            filter_query = {'slug': instance.slug} if instance.slug else {'id': instance.id}
            db.core_tour.replace_one(filter_query, doc, upsert=True)
        elif model_name == 'BlogPost':
            doc = blog_to_dict(instance)
            filter_query = {'slug': instance.slug} if instance.slug else {'id': instance.id}
            db.core_blogpost.replace_one(filter_query, doc, upsert=True)
        elif model_name == 'HeroSection':
            doc = hero_to_dict(instance)
            db.core_herosection.replace_one({'id': instance.id}, doc, upsert=True)
        elif model_name == 'GuestReview':
            doc = review_to_dict(instance)
            db.core_guestreview.replace_one({'id': instance.id}, doc, upsert=True)
        elif model_name == 'SafariBooking':
            doc = booking_to_dict(instance)
            db.core_safaribooking.replace_one({'id': instance.id}, doc, upsert=True)
        return True
    except Exception as e:
        logger.error(f"Error syncing {instance.__class__.__name__} to MongoDB Atlas: {e}")
        return False

def delete_model_from_mongo(instance):
    """
    Called whenever an instance is deleted in Django Admin.
    Deletes the corresponding document from MongoDB Atlas in real time.
    """
    db = get_mongo_db()
    if db is None:
        return False
    try:
        model_name = instance.__class__.__name__
        filter_query = {'slug': instance.slug} if getattr(instance, 'slug', None) else {'id': instance.id}
        if model_name == 'SafariPackage':
            db.core_safaripackage.delete_many(filter_query)
            db.packages.delete_many(filter_query)
        elif model_name == 'Tour':
            db.core_tour.delete_many(filter_query)
        elif model_name == 'BlogPost':
            db.core_blogpost.delete_many(filter_query)
        elif model_name == 'HeroSection':
            db.core_herosection.delete_many({'id': instance.id})
        elif model_name == 'GuestReview':
            db.core_guestreview.delete_many({'id': instance.id})
        elif model_name == 'SafariBooking':
            db.core_safaribooking.delete_many({'id': instance.id})
        return True
    except Exception as e:
        logger.error(f"Error deleting {instance.__class__.__name__} from MongoDB Atlas: {e}")
        return False

# ==============================================================================
# Bi-Directional Database Hydration (Cold-Start & Seeding)
# ==============================================================================

def sync_all_from_mongo_to_sqlite():
    """
    Loads latest documents from MongoDB Atlas into SQLite so Django Admin
    always displays the true live database content upon cold start.
    """
    db = get_mongo_db()
    if db is None:
        return False

    try:
        from .models import SafariPackage, Tour, BlogPost, HeroSection, GuestReview

        # 1. Sync Safari Packages
        mongo_pkgs = list(db.core_safaripackage.find()) or list(db.packages.find())
        if mongo_pkgs:
            for d in mongo_pkgs:
                slug_val = d.get('slug') or str(d.get('id', ''))
                SafariPackage.objects.update_or_create(
                    slug=slug_val,
                    defaults={
                        'title': d.get('title', ''),
                        'subtitle': d.get('subtitle', ''),
                        'imageUrl': d.get('imageUrl', ''),
                        'image_urls': d.get('image_urls', ''),
                        'description': d.get('description', ''),
                        'category': d.get('category', 'half-day'),
                        'category_label': d.get('category_label', 'HALF-DAY GAME DRIVE'),
                        'tag_class': d.get('tag_class', 'tag-sage'),
                        'price_type': d.get('price_type', 'jeep_only'),
                        'price': str(d.get('price', '$120')),
                        'price_unit': d.get('price_unit', 'per 4x4 jeep (up to 6 guests)'),
                        'mealPrice': str(d.get('mealPrice', '0')),
                        'ticketPrice': str(d.get('ticketPrice', '0')),
                        'childTicketPrice': str(d.get('childTicketPrice', '20')),
                        'includes_tickets': bool(d.get('includes_tickets', False)),
                        'ticket_addon_price': d.get('ticket_addon_price', ''),
                        'includes_breakfast': bool(d.get('includes_breakfast', False)),
                        'breakfast_addon_price': d.get('breakfast_addon_price', ''),
                        'duration': d.get('duration', '5 Hours'),
                        'vehicle': d.get('vehicle', 'Private 4x4 Jeep'),
                        'inclusions': d.get('inclusions', ''),
                        'exclusions': d.get('exclusions', ''),
                        'highlights': d.get('highlights', ''),
                        'featured': bool(d.get('featured', False)),
                    }
                )

        # 2. Sync Tours
        mongo_tours = list(db.core_tour.find())
        if mongo_tours:
            for t in mongo_tours:
                slug_val = t.get('slug') or str(t.get('id', ''))
                Tour.objects.update_or_create(
                    slug=slug_val,
                    defaults={
                        'title': t.get('title', ''),
                        'route': t.get('route', ''),
                        'price': str(t.get('price', '280')),
                        'duration': t.get('duration', '5 Days / 4 Nights'),
                        'imageUrl': t.get('imageUrl', ''),
                        'isFeatured': bool(t.get('isFeatured', True)),
                        'description': t.get('description', ''),
                        'longDescription': t.get('longDescription', ''),
                        'highlights': t.get('highlights', ''),
                        'inclusions': t.get('inclusions', ''),
                        'exclusions': t.get('exclusions', ''),
                        'seoKeywords': t.get('seoKeywords', ''),
                        'itinerary_json': t.get('itinerary_json', ''),
                    }
                )

        # 3. Sync Blog Posts
        mongo_blogs = list(db.core_blogpost.find())
        if mongo_blogs:
            for b in mongo_blogs:
                slug_val = b.get('slug') or str(b.get('id', ''))
                BlogPost.objects.update_or_create(
                    slug=slug_val,
                    defaults={
                        'title': b.get('title', ''),
                        'category': b.get('category', 'WILDLIFE LOG'),
                        'author': b.get('author', 'Discoveryala Naturalist'),
                        'imageUrl': b.get('imageUrl', ''),
                        'content': b.get('content', ''),
                        'featured': bool(b.get('featured', False)),
                    }
                )

        # 4. Sync Hero Sections
        mongo_heroes = list(db.core_herosection.find())
        if mongo_heroes:
            for h in mongo_heroes:
                HeroSection.objects.update_or_create(
                    id=h.get('id', 1),
                    defaults={
                        'title': h.get('title', 'WILD YALA SAFARIS'),
                        'subtitle': h.get('subtitle', "Ceylon's premier 4x4 game drives & luxury glamping."),
                        'badge_text': h.get('badge_text', '🌿 YALA LEOPARD TRACKS'),
                        'imageUrl': h.get('imageUrl', '') or h.get('bg_image_url', ''),
                        'button_primary_text': h.get('button_primary_text', 'EXPLORE PACKAGES'),
                        'button_primary_url': h.get('button_primary_url', '/packages/'),
                        'button_secondary_text': h.get('button_secondary_text', 'BOOK SAFARI'),
                        'button_secondary_url': h.get('button_secondary_url', '/contact/'),
                        'is_active': bool(h.get('is_active', True)),
                    }
                )

        # 5. Sync Guest Reviews
        mongo_revs = list(db.core_guestreview.find())
        if mongo_revs:
            for r in mongo_revs:
                GuestReview.objects.update_or_create(
                    id=r.get('id', 1),
                    defaults={
                        'category': r.get('category', 'leopard'),
                        'name': r.get('name', ''),
                        'origin': r.get('origin', 'London, UK'),
                        'date': r.get('date', 'August 2026'),
                        'package': r.get('package', 'Yala Block 1 Morning Leopard Game Drive'),
                        'rating': int(r.get('rating', 5)),
                        'comment': r.get('comment', ''),
                        'verified': bool(r.get('verified', True)),
                        'avatar_url': r.get('avatar_url', ''),
                        'photo_url': r.get('photo_url', ''),
                        'source': r.get('source', 'Google Maps'),
                    }
                )

        return True
    except Exception as e:
        logger.error(f"Error hydrating SQLite from MongoDB Atlas: {e}")
        return False

def sync_all_from_sqlite_to_mongo():
    """
    Pushes all existing Django models from SQLite to MongoDB Atlas.
    """
    db = get_mongo_db()
    if db is None:
        return False

    try:
        from .models import SafariPackage, Tour, BlogPost, HeroSection, GuestReview, SafariBooking

        for pkg in SafariPackage.objects.all():
            sync_model_to_mongo(pkg)
        for tour in Tour.objects.all():
            sync_model_to_mongo(tour)
        for blog in BlogPost.objects.all():
            sync_model_to_mongo(blog)
        for hero in HeroSection.objects.all():
            sync_model_to_mongo(hero)
        for rev in GuestReview.objects.all():
            sync_model_to_mongo(rev)
        for book in SafariBooking.objects.all():
            sync_model_to_mongo(book)
        return True
    except Exception as e:
        logger.error(f"Error seeding MongoDB Atlas from SQLite: {e}")
        return False

# ==============================================================================
# MongoDB Fetch Helpers (For Views)
# ==============================================================================

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

