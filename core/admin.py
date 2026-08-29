from django.contrib import admin
from .models import SafariPackage, SafariBooking, BlogPost, HeroSection, Tour



# Customize Django Admin Panel Titles & Branding
admin.site.site_header = "Discoveryala Administration"
admin.site.site_title = "Discoveryala Admin"
admin.site.index_title = "Safari Packages & Eco-Expeditions Desk"

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'route', 'duration', 'price', 'isFeatured', 'updated_at')
    list_display_links = ('title', 'slug')
    list_editable = ('isFeatured', 'price')
    list_filter = ('isFeatured', 'created_at')
    search_fields = ('title', 'slug', 'route', 'description', 'longDescription')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    fieldsets = (
        ('1. Tour Overview & Route', {
            'fields': ('title', 'slug', 'route', 'duration', 'price', 'isFeatured')
        }),
        ('2. Cover Image', {
            'description': 'Upload image file from device OR paste Cloudinary / image URL link below.',
            'fields': ('image_file', 'imageUrl')
        }),
        ('3. Tour Story & Detailed Descriptions', {
            'fields': ('description', 'longDescription', 'highlights', 'inclusions', 'exclusions', 'seoKeywords')
        }),
        ('4. Day-by-Day Itinerary (JSON)', {
            'description': 'Formatted JSON array of itinerary items with day, title, and description.',
            'fields': ('itinerary_json',)
        }),
    )

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'badge_text', 'is_active', 'updated_at')
    list_display_links = ('title',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle', 'badge_text')
    list_per_page = 20

    fieldsets = (
        ('1. Hero Headlines & Badge Tag', {
            'fields': ('title', 'subtitle', 'badge_text', 'is_active')
        }),
        ('2. Background Image Settings', {
            'description': 'Upload a new background image from your device OR paste a direct Cloudinary URL link below.',
            'fields': ('image_file', 'imageUrl')
        }),
        ('3. Call-to-Action (CTA) Buttons', {
            'fields': (
                'button_primary_text', 'button_primary_url',
                'button_secondary_text', 'button_secondary_url'
            )
        }),
    )

@admin.register(SafariPackage)
class SafariPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'price_type', 'price', 'mealPrice', 'ticketPrice', 'childTicketPrice', 'featured', 'updated_at')
    list_display_links = ('title', 'slug')
    list_editable = ('category', 'price_type', 'price', 'mealPrice', 'ticketPrice', 'childTicketPrice', 'featured')
    list_filter = ('category', 'price_type', 'includes_tickets', 'includes_breakfast', 'featured')
    search_fields = ('title', 'slug', 'subtitle', 'description', 'highlights', 'inclusions', 'exclusions')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    fieldsets = (
        ('1. Basic Package Information', {
            'description': 'Upload a local image file OR paste primary Cloudinary image URL link below. Add extra gallery image URLs into Additional Image URLs.',
            'fields': ('title', 'slug', 'subtitle', 'category', 'category_label', 'tag_class', 'image_file', 'imageUrl', 'image_urls', 'description', 'featured')
        }),
        ('2. Pricing & Add-on Controls', {
            'description': 'Configure base price, meal price, adult ticket price, child ticket price, and optional add-on options.',
            'fields': (
                'price_type', 'price', 'price_unit',
                'mealPrice', 'ticketPrice', 'childTicketPrice',
                'includes_tickets', 'ticket_addon_price',
                'includes_breakfast', 'breakfast_addon_price'
            )
        }),
        ('3. Package Content & Specifications', {
            'fields': ('duration', 'vehicle', 'highlights', 'inclusions', 'exclusions')
        }),
    )

@admin.register(SafariBooking)
class SafariBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'package_title', 'safari_date', 'guests', 'adult_guests', 'child_guests', 'under6_guests', 'meal_count', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'safari_date', 'include_meals', 'include_tickets')
    search_fields = ('full_name', 'email', 'phone_number', 'package_title', 'country')
    list_editable = ('status',)
    readonly_fields = ('created_at',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'author', 'featured', 'created_at')
    list_display_links = ('title', 'slug')
    list_editable = ('category', 'author', 'featured')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('title', 'slug', 'content', 'author', 'category')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    fieldsets = (
        ('1. Article Details & Branding', {
            'fields': ('title', 'slug', 'category', 'author', 'featured')
        }),
        ('2. Article Cover Image', {
            'description': 'Upload an image file from your computer/phone OR paste a direct Cloudinary URL.',
            'fields': ('image_file', 'imageUrl')
        }),
        ('3. Article Story Content', {
            'fields': ('content',)
        }),
    )

from .models import GuestReview

@admin.register(GuestReview)
class GuestReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'rating', 'category', 'verified', 'source', 'created_at')
    list_filter = ('category', 'rating', 'verified', 'source')
    search_fields = ('name', 'origin', 'comment', 'package')
    list_editable = ('rating', 'verified')
    list_per_page = 20



