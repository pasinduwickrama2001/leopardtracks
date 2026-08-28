import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SafariPackage, Tour, BlogPost, HeroSection, GuestReview, SafariBooking
from .mongodb import sync_model_to_mongo, delete_model_from_mongo

logger = logging.getLogger(__name__)

# Models to synchronize in real time with MongoDB Atlas
SYNC_MODELS = [SafariPackage, Tour, BlogPost, HeroSection, GuestReview, SafariBooking]

for model_cls in SYNC_MODELS:
    @receiver(post_save, sender=model_cls, weak=False)
    def handle_mongo_post_save(sender, instance, **kwargs):
        try:
            sync_model_to_mongo(instance)
        except Exception as e:
            logger.error(f"Failed to sync {sender.__name__} save to MongoDB: {e}")

    @receiver(post_delete, sender=model_cls, weak=False)
    def handle_mongo_post_delete(sender, instance, **kwargs):
        try:
            delete_model_from_mongo(instance)
        except Exception as e:
            logger.error(f"Failed to sync {sender.__name__} delete to MongoDB: {e}")
