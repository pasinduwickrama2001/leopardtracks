import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SafariPackage, Tour, BlogPost, HeroSection, GuestReview, SafariBooking
from .mongodb import sync_model_to_mongo, delete_model_from_mongo, is_mongo_sync_paused

logger = logging.getLogger(__name__)

SYNC_MODELS = (SafariPackage, Tour, BlogPost, HeroSection, GuestReview, SafariBooking)

@receiver(post_save)
def handle_mongo_post_save(sender, instance, **kwargs):
    if sender in SYNC_MODELS:
        if is_mongo_sync_paused():
            return
        try:
            sync_model_to_mongo(instance)
        except Exception as e:
            logger.error(f"Failed to sync {sender.__name__} save to MongoDB: {e}")

@receiver(post_delete)
def handle_mongo_post_delete(sender, instance, **kwargs):
    if sender in SYNC_MODELS:
        if is_mongo_sync_paused():
            return
        try:
            delete_model_from_mongo(instance)
        except Exception as e:
            logger.error(f"Failed to sync {sender.__name__} delete to MongoDB: {e}")

