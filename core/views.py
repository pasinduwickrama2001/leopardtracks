from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import SafariPackage, SafariBooking, BlogPost, HeroSection, Tour, GuestReview



def home(request):
    try:
        all_heroes = list(HeroSection.objects.all())
        active_heroes = [h for h in all_heroes if getattr(h, 'is_active', True)]
        hero = active_heroes[0] if active_heroes else (all_heroes[0] if all_heroes else None)
    except Exception:
        hero = None

    # Fetch Dynamic Counts from Database with Safe Exception Handling
    try:
        total_packages = SafariPackage.objects.count()
        total_tours = Tour.objects.count()
        total_blogs = BlogPost.objects.count()
        total_reviews = GuestReview.objects.count()
    except Exception:
        total_packages = total_tours = total_blogs = total_reviews = 0

    # Fetch ALL Dynamic Safari Packages from Database
    packages_list = []
    try:
        packages_qs = SafariPackage.objects.all()
        for pkg in packages_qs:
            packages_list.append({
                'id': pkg.id,
                'title': pkg.title,
                'subtitle': pkg.subtitle,
                'slug': pkg.slug,
                'imageUrl': pkg.imageUrl or '/static/images/yala-tent.jpg',
                'description': pkg.description,
                'category_label': pkg.category_label,
                'tag_class': pkg.tag_class,
                'clean_price': pkg.get_clean_price(),
                'price_unit': pkg.price_unit,
                'duration': pkg.duration,
                'vehicle': pkg.vehicle,
                'inclusions_list': pkg.get_inclusions_list()[:3],
            })
    except Exception:
        packages_list = []

    # Fetch ALL Dynamic Island Round Tours from Database
    tours_list = []
    try:
        tours_qs = Tour.objects.all()
        for tr in tours_qs:
            tours_list.append({
                'id': tr.id,
                'title': tr.title,
                'slug': tr.slug,
                'route': tr.route,
                'duration': tr.duration,
                'clean_price': tr.get_clean_price(),
                'imageUrl': tr.get_tour_image_url(),
                'description': tr.description,
                'highlights_list': tr.get_highlights_list()[:3],
            })
    except Exception:
        tours_list = []

    # Fetch ALL Dynamic Wildlife Field Journal Blogs from Database & Shuffle Randomly
    blogs_list = []
    try:
        blogs_qs = list(BlogPost.objects.all())
        import random
        random.shuffle(blogs_qs)

        for b in blogs_qs:
            paragraphs = b.get_paragraphs()
            excerpt = paragraphs[0] if paragraphs else b.content[:140] + "..."
            blogs_list.append({
                'id': b.id,
                'title': b.title,
                'slug': b.slug,
                'category': b.category,
                'author': b.author,
                'imageUrl': b.imageUrl or '/static/images/yala-wildlife-hero.jpg',
                'excerpt': excerpt[:140] + ("..." if len(excerpt) > 140 else ""),
                'created_at': b.created_at.strftime('%b %d, %Y') if getattr(b, 'created_at', None) else 'Aug 2026',
            })
    except Exception:
        blogs_list = []

    # Fetch ALL Verified Guest Reviews & Testimonials from Database
    reviews_list = []
    try:
        all_reviews = list(GuestReview.objects.all())
        verified_reviews = [r for r in all_reviews if getattr(r, 'verified', True)]
        reviews_qs = verified_reviews[:6] if verified_reviews else all_reviews[:6]

        for r in reviews_qs:
            reviews_list.append({
                'name': r.name,
                'origin': r.origin,
                'package': r.package,
                'rating': r.rating,
                'rating_stars': range(r.rating),
                'comment': r.comment,
                'source': r.source,
                'date': r.date,
            })
    except Exception:
        reviews_list = []

    # Dynamic Stats Summary driven by database counts
    stats_summary = [
        {'value': f"{total_packages}+", 'label': 'Curated Safari Packages', 'icon': 'fa-truck-monster'},
        {'value': '98%', 'label': 'Leopard Sighting Success', 'icon': 'fa-paw'},
        {'value': f"{total_reviews}+", 'label': 'Verified Guest Reviews', 'icon': 'fa-star'},
        {'value': '15+', 'label': 'Years Eco-Expeditions', 'icon': 'fa-calendar-check'},
    ]

    context = {
        'title': 'Yala Leopard Tracks | Yala National Park Safaris & Luxury Camping Sri Lanka',
        'hero': hero,
        'home_packages': packages_list,
        'home_tours': tours_list,
        'home_blogs': blogs_list,
        'home_reviews': reviews_list,
        'stats_summary': stats_summary,
        'total_packages_count': total_packages,
        'total_tours_count': total_tours,
        'total_blogs_count': total_blogs,
        'total_reviews_count': total_reviews,
    }
    return render(request, 'core/home.html', context)





def packages(request):
    packages_queryset = SafariPackage.objects.all()
    
    # Process inclusions, exclusions, and highlights lists for template display
    packages_list = []
    for pkg in packages_queryset:
        clean_p = pkg.get_clean_price()
        packages_list.append({
            'id': pkg.id,
            'title': pkg.title,
            'subtitle': pkg.subtitle,
            'slug': pkg.slug,
            'imageUrl': pkg.imageUrl,
            'description': pkg.description,
            'category': pkg.category,
            'category_label': pkg.category_label,
            'tag_class': pkg.tag_class,
            'price_type': pkg.price_type,
            'price': clean_p,
            'get_clean_price': clean_p,
            'price_unit': pkg.price_unit,
            'mealPrice': pkg.mealPrice,
            'ticketPrice': pkg.ticketPrice,
            'includes_tickets': pkg.includes_tickets,
            'ticket_addon_price': pkg.ticket_addon_price,
            'includes_breakfast': pkg.includes_breakfast,
            'breakfast_addon_price': pkg.breakfast_addon_price,
            'duration': pkg.duration,
            'vehicle': pkg.vehicle,
            'inclusions': pkg.get_inclusions_list(),
            'exclusions': pkg.get_exclusions_list(),
            'highlights_list': pkg.get_highlights_list(),
            'highlights': pkg.highlights,
            'featured': pkg.featured
        })

    featured_package = next((p for p in packages_list if p.get('featured')), packages_list[0] if packages_list else None)

    context = {
        'title': 'Yala Safari Packages & Expeditions | Yala Leopard Tracks',
        'packages_list': packages_list,
        'featured_package': featured_package,
    }
    return render(request, 'core/packages.html', context)

def package_detail(request, slug):
    package = SafariPackage.objects.filter(slug=slug).first()
    if not package and slug.isdigit():
        package = SafariPackage.objects.filter(id=int(slug)).first()
        
    if not package:
        return redirect('packages')

    other_packages = SafariPackage.objects.exclude(id=package.id)[:3]

    context = {
        'title': f'{package.title} | Yala Leopard Tracks',
        'package': package,
        'inclusions_list': package.get_inclusions_list(),
        'exclusions_list': package.get_exclusions_list(),
        'highlights_list': package.get_highlights_list(),
        'image_urls_list': package.get_image_urls_list(),
        'other_packages': other_packages
    }
    return render(request, 'core/package_detail.html', context)

def create_booking(request):
    if request.method == 'POST':
        try:
            package_title = request.POST.get('package_title', 'Safari Booking')
            full_name = request.POST.get('full_name', '')
            country = request.POST.get('country', '')
            email = request.POST.get('email', '')
            phone_code = request.POST.get('phone_code', '+94')
            phone_number = request.POST.get('phone_number', '')
            
            safari_date = request.POST.get('safari_date')
            adult_guests = int(request.POST.get('adult_guests', 2) or 2)
            child_guests = int(request.POST.get('child_guests', 0) or 0)
            under6_guests = int(request.POST.get('under6_guests', 0) or 0)
            guests = adult_guests + child_guests + under6_guests
            if guests == 0:
                guests = int(request.POST.get('guests', 2) or 2)
            
            include_meals = request.POST.get('include_meals') in ['true', 'on', 'True', '1']
            meal_count = int(request.POST.get('meal_count', 0) or 0) if include_meals else 0
            include_tickets = request.POST.get('include_tickets') in ['true', 'on', 'True', '1']
            
            base_price = float(request.POST.get('base_price', 0.0) or 0)
            meals_price_total = float(request.POST.get('meals_price_total', 0.0) or 0)
            tickets_price_total = float(request.POST.get('tickets_price_total', 0.0) or 0)
            total_price = float(request.POST.get('total_price', 0.0) or 0)
            message = request.POST.get('message', '')

            booking = SafariBooking.objects.create(
                package_title=package_title,
                full_name=full_name,
                country=country,
                email=email,
                phone_code=phone_code,
                phone_number=phone_number,
                safari_date=safari_date,
                guests=guests,
                adult_guests=adult_guests,
                child_guests=child_guests,
                under6_guests=under6_guests,
                include_meals=include_meals,
                meal_count=meal_count,
                meals_price_total=meals_price_total,
                include_tickets=include_tickets,
                tickets_price_total=tickets_price_total,
                base_price=base_price,
                total_price=total_price,
                message=message,
                status='Pending'
            )

            # Send Rich HTML Email Confirmation to Guest & Notification Email to Admin
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings

                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Yala Leopard Tracks <yalaleopardtracks@gmail.com>')
                admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'yalaleopardtracks@gmail.com')
                if getattr(settings, 'EMAIL_HOST_USER', ''):
                    admin_email = getattr(settings, 'EMAIL_HOST_USER')

                # 1. Confirmation Email to Guest (Rich HTML Theme)
                guest_subject = f"Safari Reservation Received - {package_title} | Yala Leopard Tracks"
                
                guest_text = f"""Ayubowan {full_name}!

Thank you for reserving your safari expedition with Yala Leopard Tracks!
Booking Reference: #{booking.id}
Package: {package_title}
Safari Date: {safari_date}
Guests: {guests}
Total Estimated Amount: ${total_price:.2f}

Hotline / WhatsApp: +94 778158004
Email: yalaleopardtracks@gmail.com

Our safari coordinator desk will contact you shortly to confirm pickup details.
Yala Leopard Tracks Expeditions Team
"""

                guest_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Safari Reservation Confirmation</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Playfair+Display:wght@700;900&display=swap');
    body {{ font-family: 'Poppins', Arial, sans-serif; background-color: #FAF6EE; color: #233325; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }}
    .email-wrapper {{ background-color: #FAF6EE; padding: 24px 12px; }}
    .email-container {{ max-width: 620px; margin: 0 auto; background: #FFFFFF; border-radius: 24px; overflow: hidden; border: 1px solid rgba(71, 81, 40, 0.18); box-shadow: 0 16px 45px rgba(18, 33, 24, 0.08); }}
    .email-header {{ background-color: #122118; padding: 38px 28px 30px; text-align: center; color: #FFFFFF; border-bottom: 3px solid #D4AF37; position: relative; }}
    .brand-pill {{ display: inline-block; background: rgba(212, 175, 55, 0.15); color: #D4AF37; font-size: 10px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; padding: 6px 18px; border-radius: 30px; border: 1px solid rgba(212, 175, 55, 0.35); margin-bottom: 14px; }}
    .header-title {{ font-family: 'Playfair Display', Georgia, serif; font-size: 25px; font-weight: 900; letter-spacing: 1px; margin: 0; color: #FFFFFF; text-transform: uppercase; }}
    .header-sub {{ font-size: 13px; color: #E7EBD9; margin-top: 8px; font-weight: 600; letter-spacing: 0.5px; }}
    .ref-badge {{ display: inline-block; background: rgba(255, 255, 255, 0.1); color: #D4AF37; font-size: 12px; font-weight: 700; padding: 4px 14px; border-radius: 12px; margin-top: 10px; border: 1px dashed rgba(212, 175, 55, 0.4); }}
    .email-body {{ padding: 36px 30px; background-color: #FAF6EE; }}
    .greeting {{ font-family: 'Playfair Display', Georgia, serif; font-size: 22px; font-weight: 900; color: #475128; margin-bottom: 10px; }}
    .intro-p {{ font-size: 14px; line-height: 1.7; color: #333333; margin-bottom: 26px; }}
    .card-box {{ background: #FFFFFF; border-radius: 18px; padding: 24px; border: 1px solid rgba(71, 81, 40, 0.14); margin-bottom: 22px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }}
    .card-title {{ font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: #606C38; margin-bottom: 16px; border-bottom: 1px solid rgba(71, 81, 40, 0.1); padding-bottom: 8px; display: flex; align-items: center; justify-content: space-between; }}
    .info-row {{ display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 12px; line-height: 1.4; border-bottom: 1px dashed rgba(71, 81, 40, 0.08); padding-bottom: 8px; }}
    .info-row:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
    .info-label {{ color: #666666; font-weight: 500; }}
    .info-value {{ font-weight: 700; color: #233325; text-align: right; }}
    .badge-green {{ background: #E7EBD9; color: #475128; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 10px; text-transform: uppercase; }}
    .total-box {{ background: #475128; color: #FFFFFF; border-radius: 16px; padding: 20px 22px; margin-top: 16px; border: 1px solid rgba(212, 175, 55, 0.35); box-shadow: 0 6px 20px rgba(71, 81, 40, 0.2); }}
    .total-amount {{ font-family: 'Playfair Display', Georgia, serif; font-size: 26px; font-weight: 900; color: #D4AF37; float: right; margin-top: -2px; }}
    .phone-contact-box {{ background: linear-gradient(135deg, #606C38 0%, #475128 100%); color: #FFFFFF; border-radius: 18px; padding: 24px; text-align: center; margin-bottom: 22px; box-shadow: 0 10px 25px rgba(96, 108, 56, 0.25); border: 1px solid rgba(212, 175, 55, 0.3); }}
    .phone-number-btn {{ display: inline-block; background: #D4AF37; color: #122118; text-decoration: none; padding: 12px 28px; border-radius: 30px; font-weight: 900; font-size: 15px; margin-top: 12px; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }}
    .note-box {{ background: #E7EBD9; border-radius: 14px; padding: 18px; font-size: 13px; color: #475128; margin-top: 22px; line-height: 1.65; border-left: 4px solid #606C38; }}
    .email-footer {{ background-color: #122118; padding: 30px 24px; text-align: center; font-size: 12px; color: #999999; border-top: 1px solid rgba(255,255,255,0.06); }}
    .footer-link {{ color: #D4AF37; text-decoration: none; font-weight: 700; }}
</style>
</head>
<body>
<div class="email-wrapper">
    <div class="email-container">
        <div class="email-header">
            <span class="brand-pill">YALA LEOPARD TRACKS EXPEDITIONS</span>
            <h1 class="header-title">🐆 SAFARI RESERVATION CONFIRMED</h1>
            <div class="header-sub">Yala & Bundala National Park Game Drives</div>
            <div class="ref-badge">Booking Reference: #{booking.id}</div>
        </div>
        
        <div class="email-body">
            <div class="greeting">Ayubowan, {full_name}! 🌿</div>
            <p class="intro-p">Thank you for reserving your safari expedition with <strong>Yala Leopard Tracks</strong>! We have received your booking request and our naturalist desk is preparing your private 4x4 game drive itinerary.</p>
            
            <!-- Reservation Details Card -->
            <div class="card-box">
                <div class="card-title"><span>01. Safari Expedition Summary</span> <span class="badge-green">CONFIRMED</span></div>
                <div class="info-row"><span class="info-label">Safari Package:</span><span class="info-value">{package_title}</span></div>
                <div class="info-row"><span class="info-label">Safari Date:</span><span class="info-value" style="color: #606C38; font-weight: 800;">{safari_date}</span></div>
                <div class="info-row"><span class="info-label">Guests Count:</span><span class="info-value">{guests} Guest(s)</span></div>
                <div class="info-row"><span class="info-label">Hotel Pickup & Drop:</span><span class="info-value" style="color: #606C38;">FREE (Yala / Tissa / Kirinda)</span></div>
            </div>

            <!-- Guest Info Card -->
            <div class="card-box">
                <div class="card-title">02. Guest Contact Details</div>
                <div class="info-row"><span class="info-label">Full Name:</span><span class="info-value">{full_name}</span></div>
                <div class="info-row"><span class="info-label">Country:</span><span class="info-value">{country}</span></div>
                <div class="info-row"><span class="info-label">Email:</span><span class="info-value">{email}</span></div>
                <div class="info-row"><span class="info-label">Phone Number:</span><span class="info-value">{phone_code} {phone_number}</span></div>
            </div>

            <!-- Pricing Summary Card -->
            <div class="card-box">
                <div class="card-title">03. Estimated Pricing Breakdown</div>
                <div class="info-row"><span class="info-label">Base Safari Game Drive:</span><span class="info-value">${base_price:.2f}</span></div>
                <div class="info-row"><span class="info-label">Meal / Breakfast Add-ons:</span><span class="info-value">{'Included ($0.00)' if include_meals and meals_price_total == 0 else ('$' + f'{meals_price_total:.2f}') if include_meals else 'Not Selected'}</span></div>
                <div class="info-row"><span class="info-label">National Park Entrance Tickets:</span><span class="info-value">{'Included ($0.00)' if include_tickets and tickets_price_total == 0 else ('$' + f'{tickets_price_total:.2f}') if include_tickets else 'Not Selected'}</span></div>
                
                <div class="total-box">
                    <span class="total-amount">${total_price:.2f}</span>
                    <span style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; line-height: 28px;">Total Estimated Amount</span>
                </div>
            </div>

            {f'<div class="card-box"><div class="card-title">04. Special Requests / Notes</div><div style="font-size: 13px; color: #444444; font-style: italic; line-height: 1.6;">"{message}"</div></div>' if message else ''}

            <!-- Direct Phone / WhatsApp Contact Callout Card -->
            <div class="phone-contact-box">
                <div style="font-size: 11px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; color: #E7EBD9;">NEED IMMEDIATE SAFARI ASSISTANCE?</div>
                <div style="font-size: 14px; line-height: 1.5; margin-bottom: 8px;">Call or WhatsApp our 24/7 Safari Desk directly:</div>
                <a href="https://wa.me/94778158004" class="phone-number-btn">📞 CALL / WHATSAPP: +94 778158004</a>
            </div>

            <div class="note-box">
                📌 <strong>Next Steps:</strong> Our senior safari coordinator desk will contact you shortly via Email / WhatsApp (<a href="https://wa.me/94778158004" style="color: #475128; font-weight: 700;">+94 778158004</a>) to verify your hotel pickup location and driver vehicle assignment.
            </div>
        </div>

        <div class="email-footer">
            <p style="margin: 0 0 8px 0; font-weight: 700; color: #FFFFFF; font-size: 13px;">Yala Leopard Tracks Expeditions & Luxury Safaris</p>
            <p style="margin: 0 0 10px 0;">Yala National Park Buffer Zone, Tissamaharama, Sri Lanka</p>
            <p style="margin: 0 0 12px 0; font-weight: 800; color: #D4AF37; font-size: 13px;">Hotline / WhatsApp: +94 778158004</p>
            <p style="margin: 0;">Email: <a href="mailto:yalaleopardtracks@gmail.com" class="footer-link">yalaleopardtracks@gmail.com</a> | Web: <a href="https://yalaleopardtracks.com" class="footer-link">yalaleopardtracks.com</a></p>
        </div>
    </div>
</div>
</body>
</html>"""

                msg_guest = EmailMultiAlternatives(guest_subject, guest_text, from_email, [email])
                msg_guest.attach_alternative(guest_html, "text/html")
                msg_guest.send(fail_silently=False)

                # 2. Notification Email to Admin (Rich HTML Theme)
                admin_subject = f"🚨 NEW BOOKING ALERT: {package_title} - {full_name} ({safari_date})"
                admin_text = f"""NEW SAFARI RESERVATION ALERT!
Customer: {full_name} ({country})
Email: {email} | Phone: {phone_code} {phone_number}
Package: {package_title}
Date: {safari_date} | Guests: {guests}
Total: ${total_price:.2f}

Safari Desk Hotline: +94 778158004
"""

                admin_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{ font-family: 'Poppins', Arial, sans-serif; background-color: #FAF6EE; color: #233325; margin: 0; padding: 20px; }}
    .admin-card {{ max-width: 600px; margin: 0 auto; background: #FFFFFF; border-radius: 20px; padding: 30px; border: 1px solid rgba(71,81,40,0.2); box-shadow: 0 12px 35px rgba(0,0,0,0.08); }}
    .alert-header {{ background: #122118; color: #FFFFFF; padding: 18px 24px; border-radius: 14px; font-size: 15px; font-weight: 800; letter-spacing: 1px; margin-bottom: 22px; border-left: 4px solid #D4AF37; }}
    .alert-price {{ float: right; background: #D4AF37; color: #122118; padding: 4px 14px; border-radius: 12px; font-weight: 900; font-size: 16px; }}
    .row {{ margin-bottom: 12px; font-size: 14px; border-bottom: 1px dashed rgba(71,81,40,0.15); padding-bottom: 8px; display: flex; justify-content: space-between; }}
    .label {{ font-weight: 600; color: #475128; width: 140px; }}
    .val {{ color: #233325; font-weight: 700; text-align: right; }}
    .btn-admin {{ display: block; background: #606C38; color: #FFFFFF; text-decoration: none; padding: 14px 24px; border-radius: 30px; font-weight: 800; margin-top: 24px; text-align: center; font-size: 14px; letter-spacing: 1px; box-shadow: 0 6px 20px rgba(96,108,56,0.25); }}
</style>
</head>
<body>
<div class="admin-card">
    <div class="alert-header">
        <span class="alert-price">${total_price:.2f}</span>
        🚨 NEW SAFARI RESERVATION
    </div>

    <div style="margin-bottom: 22px; font-size: 17px; font-weight: 800; color: #233325; border-bottom: 2px solid #606C38; padding-bottom: 10px;">
        Package: {package_title}
    </div>

    <div class="row"><span class="label">Customer Name:</span><span class="val">{full_name}</span></div>
    <div class="row"><span class="label">Country:</span><span class="val">{country}</span></div>
    <div class="row"><span class="label">Email:</span><span class="val">{email}</span></div>
    <div class="row"><span class="label">Phone Number:</span><span class="val">{phone_code} {phone_number}</span></div>
    <div class="row"><span class="label">Safari Date:</span><span class="val" style="color: #606C38; font-weight: 800;">{safari_date}</span></div>
    <div class="row"><span class="label">Guests:</span><span class="val">{guests} Guest(s)</span></div>
    <div class="row"><span class="label">Meals:</span><span class="val">{'Yes' if include_meals else 'No'} (${meals_price_total:.2f})</span></div>
    <div class="row"><span class="label">Tickets:</span><span class="val">{'Yes' if include_tickets else 'No'} (${tickets_price_total:.2f})</span></div>
    <div class="row"><span class="label">Total Price:</span><span class="val" style="font-size: 18px; color: #475128; font-weight: 900;">${total_price:.2f}</span></div>

    {f'<div style="margin-top: 16px; background: #E7EBD9; padding: 16px; border-radius: 14px; font-size: 13px; color: #475128; border-left: 3px solid #606C38;"><strong>Special Requests / Customer Note:</strong><br>"{message}"</div>' if message else ''}

    <div style="margin-top: 18px; text-align: center; font-size: 13px; font-weight: 700; color: #606C38;">
        Safari Hotline / WhatsApp: +94 778158004
    </div>

    <a href="http://127.0.0.1:8000/admin/core/safaribooking/{booking.id}/change/" class="btn-admin">OPEN IN DJANGO ADMIN PANEL</a>
</div>
</body>
</html>"""

                admin_recipients = ['yalaleopardtracks@gmail.com', 'pasinduwickramasooriya@gmail.com']
                msg_admin = EmailMultiAlternatives(admin_subject, admin_text, from_email, admin_recipients)
                msg_admin.attach_alternative(admin_html, "text/html")
                msg_admin.send(fail_silently=False)

            except Exception as mail_err:
                print('EMAIL_SEND_ERROR_LOG:', str(mail_err))

            return JsonResponse({'status': 'success', 'message': 'Thank you! Your safari reservation request has been submitted successfully. A confirmation email has been sent to your inbox.', 'booking_id': str(booking.id)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def blog(request):
    all_posts = list(BlogPost.objects.all())
    featured_post = None
    for p in all_posts:
        if getattr(p, 'featured', False):
            featured_post = p
            break
    if not featured_post and all_posts:
        featured_post = all_posts[0]

    other_posts = [p for p in all_posts if p != featured_post]

    context = {
        'title': 'Yala Wildlife Blog & Field Journal | Yala Leopard Tracks',
        'featured_post': featured_post,
        'other_posts': other_posts,
        'all_posts': all_posts
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, slug):
    all_posts = list(BlogPost.objects.all())
    post = next((p for p in all_posts if p.slug == slug), None)
    if not post and slug.isdigit():
        post = next((p for p in all_posts if str(p.pk) == slug or str(getattr(p, 'id', '')) == slug), None)
        
    if not post:
        return redirect('blog')

    recent_posts = [p for p in all_posts if p != post][:3]

    context = {
        'title': f'{post.title} | Yala Leopard Tracks Journal',
        'post': post,
        'paragraphs': post.get_paragraphs(),
        'recent_posts': recent_posts
    }
    return render(request, 'core/blog_detail.html', context)

def tours(request):
    try:
        tours_queryset = list(Tour.objects.all())
    except Exception:
        tours_queryset = []

    tours_list = []
    for item in tours_queryset:
        clean_p = item.get_clean_price()
        tours_list.append({
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'route': item.route,
            'price': clean_p,
            'get_clean_price': clean_p,
            'duration': item.duration,
            'imageUrl': item.get_tour_image_url(),
            'isFeatured': item.isFeatured,
            'description': item.description,
            'longDescription': item.longDescription,
            'highlights': item.get_highlights_list(),
            'inclusions': item.get_inclusions_list(),
            'exclusions': item.get_exclusions_list(),
            'itinerary': item.get_itinerary_list(),
        })

    context = {
        'title': 'Sri Lanka Tours & Islandwide Private Transport | Yala Leopard Tracks',
        'tours_list': tours_list,
    }
    return render(request, 'core/tours.html', context)


def tour_detail(request, slug):
    try:
        all_tours = list(Tour.objects.all())
        tour = next((t for t in all_tours if t.slug == slug), None)
        if not tour:
            tour = get_object_or_404(Tour, slug=slug)
    except Exception:
        tour = get_object_or_404(Tour, slug=slug)

    recent_tours = [t for t in all_tours if t.slug != slug][:3]

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        country = request.POST.get('country', '')
        phone_code = request.POST.get('phone_code', '+94')
        phone_number = request.POST.get('phone_number', '')
        safari_date = request.POST.get('safari_date', '')
        guests = int(request.POST.get('guests', 2) or 2)
        message = request.POST.get('message', '')

        try:
            booking = SafariBooking.objects.create(
                package_title=tour.title,
                full_name=full_name,
                country=country,
                email=email,
                phone_code=phone_code,
                phone_number=phone_number,
                safari_date=safari_date,
                guests=guests,
                adult_guests=guests,
                base_price=tour.price,
                total_price=tour.price,
                message=message,
                status='Pending'
            )

            # Send Email Confirmation to Guest & Admin in a non-blocking background thread
            def _async_send_emails():
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.conf import settings

                    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Yala Leopard Tracks <yalaleopardtracks@gmail.com>')
                    
                    guest_subject = f"Tour Reservation Confirmation - {tour.title} | Yala Leopard Tracks"
                    guest_text = f"Ayubowan {full_name}!\n\nThank you for booking {tour.title}.\nBooking Ref: #{booking.id}\nDate: {safari_date}\nGuests: {guests}\nPrice: ${tour.price}\n\nOur team will contact you shortly."
                    
                    guest_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
    body {{ font-family: Arial, sans-serif; background: #FAF6EE; padding: 20px; color: #233325; }}
    .box {{ max-width: 580px; margin: 0 auto; background: #FFF; padding: 30px; border-radius: 16px; border: 1px solid #606C38; }}
    .hdr {{ background: #122118; color: #FFF; padding: 20px; text-align: center; border-radius: 12px; font-size: 20px; font-weight: bold; }}
    .row {{ border-bottom: 1px dashed #DDD; padding: 10px 0; font-size: 14px; }}
    .lbl {{ font-weight: bold; color: #475128; }}
</style>
</head>
<body>
<div class="box">
    <div class="hdr">YALA LEOPARD TRACKS - TOUR RESERVATION</div>
    <p>Ayubowan <strong>{full_name}</strong>,</p>
    <p>Thank you for reserving your <strong>{tour.title}</strong> tour with Yala Leopard Tracks!</p>
    <div class="row"><span class="lbl">Booking Ref:</span> #{booking.id}</div>
    <div class="row"><span class="lbl">Tour Package:</span> {tour.title}</div>
    <div class="row"><span class="lbl">Tour Date:</span> {safari_date}</div>
    <div class="row"><span class="lbl">Guests:</span> {guests} Person(s)</div>
    <div class="row"><span class="lbl">Country:</span> {country}</div>
    <div class="row"><span class="lbl">Phone:</span> {phone_code} {phone_number}</div>
    <div class="row"><span class="lbl">Price:</span> ${tour.price} USD</div>
    {'<div class="row"><span class="lbl">Special Request:</span> ' + message + '</div>' if message else ''}
    <p style="margin-top:20px; font-size:13px; color:#666;">Our tour desk team will reach out to confirm your pickup location and driver details.</p>
</div>
</body>
</html>"""

                    msg = EmailMultiAlternatives(guest_subject, guest_text, from_email, [email])
                    msg.attach_alternative(guest_html, "text/html")
                    msg.send(fail_silently=True)

                    admin_subject = f"🚨 NEW TOUR BOOKING: {tour.title} - {full_name}"
                    admin_text = f"New Tour Booking: {tour.title}\nGuest: {full_name} ({email})\nPhone: {phone_code} {phone_number}\nDate: {safari_date}\nGuests: {guests}"
                    msg_admin = EmailMultiAlternatives(admin_subject, admin_text, from_email, ['yalaleopardtracks@gmail.com', 'pasinduwickramasooriya@gmail.com'])
                    msg_admin.attach_alternative(guest_html, "text/html")
                    msg_admin.send(fail_silently=True)
                except Exception as e_mail:
                    print("TOUR_BOOKING_EMAIL_ERROR:", str(e_mail))

            import threading
            threading.Thread(target=_async_send_emails, daemon=True).start()

            b_id_str = str(getattr(booking, 'id', 'CONFIRMED'))

            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.headers.get('accept', ''):
                return JsonResponse({
                    'status': 'success',
                    'guest_name': full_name,
                    'guest_email': email,
                    'booking_id': b_id_str,
                    'message': 'Reservation submitted successfully!'
                })

            return redirect(f"/tours/{slug}/")

        except Exception as e_book:
            print("TOUR_BOOKING_CREATE_ERROR:", str(e_book))
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e_book)}, status=400)
            return redirect(f"/tours/{slug}/")

    context = {
        'title': f"{tour.title} | Sri Lanka Tour Package",
        'tour': tour,
        'recent_tours': recent_tours,
        'highlights_list': tour.get_highlights_list(),
        'inclusions_list': tour.get_inclusions_list(),
        'exclusions_list': tour.get_exclusions_list(),
        'itinerary_list': tour.get_itinerary_list(),
    }
    return render(request, 'core/tour_detail.html', context)

def contact(request):
    success_message = None
    if request.method == 'POST':
        user_name = request.POST.get('full_name', '')
        user_email = request.POST.get('email_address', '')
        user_phone = request.POST.get('phone_number', '')
        inquiry_topic = request.POST.get('inquiry_topic', 'General Safari Inquiry')
        user_message = request.POST.get('message', '')

        # Send Email to Desk Admin & Guest Confirmation
        try:
            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings

            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'yalaleopardtracks@gmail.com')
            raw_admin = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', 'yalaleopardtracks@gmail.com')
            if isinstance(raw_admin, str):
                admin_recipients = [e.strip() for e in raw_admin.split(',') if e.strip()]
            else:
                admin_recipients = list(raw_admin)
            if not admin_recipients:
                admin_recipients = ['yalaleopardtracks@gmail.com']

            # 1. Admin Email Notification
            admin_subject = f"🔔 New Contact Inquiry: {inquiry_topic} - {user_name}"
            admin_body = f"""New Safari Inquiry Received via Website Contact Form:

Full Name: {user_name}
Email Address: {user_email}
Phone / WhatsApp: {user_phone}
Inquiry Topic: {inquiry_topic}

Message Details:
--------------------------------------------------
{user_message}
--------------------------------------------------
"""
            admin_msg = EmailMultiAlternatives(admin_subject, admin_body, from_email, admin_recipients)
            if user_email:
                admin_msg.reply_to = [user_email]
            admin_msg.send(fail_silently=True)

            # 2. Guest Email Confirmation
            if user_email:
                guest_subject = f"Safari Inquiry Received | Yala Leopard Tracks"
                guest_body = f"""Ayubowan {user_name}!

Thank you for contacting Yala Leopard Tracks Sri Lanka. We have received your inquiry regarding "{inquiry_topic}".

Our senior safari desk coordinator will review your request and get back to you within 15 minutes.

Summary of Your Message:
• Name: {user_name}
• Email: {user_email}
• Phone: {user_phone}
• Message: {user_message}

Warm regards,
Yala Leopard Tracks Expedition Team
Phone / WhatsApp: +94 77 815 8004
Email: yalaleopardtracks@gmail.com
Location: Yala National Park Entrance Road, Sri Lanka
"""
                guest_msg = EmailMultiAlternatives(guest_subject, guest_body, from_email, [user_email])
                guest_msg.send(fail_silently=True)

        except Exception as e:
            print("Contact form email dispatch error:", e)

        success_message = f"Thank you, {user_name}! Your safari inquiry has been received. Our Yala desk team will contact you within 15 minutes."

    context = {
        'title': 'Contact Yala Leopard Tracks | Safari Desk & Support Sri Lanka',
        'contact_info': {
            'phone': '+94 77 815 8004',
            'phone_clean': '+94778158004',
            'email': 'yalaleopardtracks@gmail.com',
            'address': 'Wickrama, Kasingama, Yala Entrance Road, Southern Province, Sri Lanka',
            'desk_hours': 'Monday – Sunday: 05:00 AM – 08:00 PM IST',
            'gate_hours': 'Park Gate Desk: 05:30 AM – 06:00 PM IST',
            'whatsapp_url': 'https://wa.me/94778158004?text=Hello%20Yala%20Leopard%20Tracks!%20I%20would%20like%20to%20inquire%20about%20safari%20packages.'
        },
        'success_message': success_message
    }
    return render(request, 'core/contact.html', context)

def about(request):
    context = {
        'title': 'About Us | Yala Leopard Tracks Eco-Expeditions Sri Lanka',
        'team_members': [
            {
                'name': 'Kapila Ratnayake',
                'role': 'Master Leopard Tracker & Lead Guide',
                'exp': '18 Years Field Experience',
                'bio': 'Born in the buffer zones of Yala, Kapila has spent 18 years mapping leopard territories across Block 1 and Block 5. His ability to decode alarm calls is unmatched.',
                'image': 'images/guaranteed-leopard.jpg'
            },
            {
                'name': 'Dr. Nimal Weerasinghe',
                'role': 'Senior Wildlife Ecologist',
                'exp': '15 Years Research Experience',
                'bio': 'Dr. Nimal oversees our Nature First policy and conducts wildlife research on sloth bear feeding corridors and elephant migration patterns.',
                'image': 'images/tailored-game-drives.jpg'
            },
            {
                'name': 'Sahan Wickramasinghe',
                'role': 'Pro Wildlife Photographer & Track Lead',
                'exp': '12 Years Field Experience',
                'bio': 'Specializing in high-end optical equipment positioning, Sahan assists wildlife photographers in capturing published shots of Yala leopards.',
                'image': 'images/bespoke-itinerary.jpg'
            }
        ],
        'pillars': [
            {
                'icon': 'fa-solid fa-seedling',
                'title': 'Nature First Policy',
                'desc': 'Strict off-road prohibition, silent electric-assist engines, zero littering, and mandatory safe distance guidelines.'
            },
            {
                'icon': 'fa-solid fa-people-roof',
                'title': 'Community Empowerment',
                'desc': '100% locally employed Southern Sri Lankan naturalist guides, trackers, and camp chefs supported by fair wages.'
            },
            {
                'icon': 'fa-solid fa-paw',
                'title': 'Leopard Territory Mapping',
                'desc': 'Decades of field tracking data mapping individual leopards in Yala Block 1 for ethical, high-probability sightings.'
            },
            {
                'icon': 'fa-solid fa-campground',
                'title': 'Eco-Luxury Glamping',
                'desc': 'Combining raw African-style tented wilderness immersion with solar power, en-suite bathrooms, and gourmet dining.'
            }
        ]
    }
    return render(request, 'core/about.html', context)

def reviews(request):
    review_success = None
    if request.method == 'POST':
        reviewer_name = request.POST.get('reviewer_name', 'Guest')
        reviewer_origin = request.POST.get('reviewer_origin', 'Google Reviewer')
        safari_package_used = request.POST.get('safari_package_used', 'Yala Safari Game Drive')
        star_rating_str = request.POST.get('star_rating', '5 Stars')
        review_text = request.POST.get('review_text', '')

        rating_num = 5
        if '4' in star_rating_str:
            rating_num = 4
        elif '3' in star_rating_str:
            rating_num = 3
        elif '2' in star_rating_str:
            rating_num = 2
        elif '1' in star_rating_str:
            rating_num = 1

        try:
            GuestReview.objects.create(
                category='leopard' if 'leopard' in safari_package_used.lower() else ('camp' if 'camp' in safari_package_used.lower() else 'drives'),
                name=reviewer_name,
                origin=reviewer_origin,
                date='August 2026',
                package=safari_package_used,
                rating=rating_num,
                comment=review_text,
                verified=True,
                source='Google Maps'
            )
            review_success = f"Thank you, {reviewer_name}! Your Google review has been recorded and is now displayed on our page."
        except Exception as e_rev:
            print("REVIEW_SAVE_ERROR:", str(e_rev))
            review_success = f"Thank you, {reviewer_name}! Your review has been recorded."

    import random
    db_reviews = list(GuestReview.objects.all())
    random.shuffle(db_reviews)

    total_reviews_count = len(db_reviews)
    avg_score = "4.9"
    if total_reviews_count > 0:
        avg_num = sum(r.rating for r in db_reviews) / float(total_reviews_count)
        avg_score = f"{avg_num:.1f}"

    context = {
        'title': 'Google Maps Verified Reviews & Wildlife Gallery | Yala Leopard Tracks',
        'rating_summary': {
            'score': avg_score,
            'stars': 5,
            'total_reviews': total_reviews_count if total_reviews_count > 0 else 6000,
            'tripadvisor_rating': '5.0 / 5.0 (Top 10% Worldwide)',
            'google_rating': f"{avg_score} / 5.0 (Google Maps Verified)"
        },
        'reviews_list': db_reviews,
        'gallery_items': [
            {
                'title': 'Yala Leopard Resting on Palu Tree',
                'category': 'leopard',
                'image': 'images/yala-leopard-card.jpg',
                'location': 'Yala Block 1',
                'credit': 'Photo by Kapila Ratnayake'
            },
            {
                'title': 'Open-Air Private 4x4 Game Viewing Jeep',
                'category': 'drives',
                'image': 'images/jeep-safari.jpg',
                'location': 'Palatupana Park Gate',
                'credit': 'Yala Leopard Tracks Fleet'
            },
            {
                'title': 'Luxury Safari Glamping Suite',
                'category': 'camp',
                'image': 'images/campsite-yala.jpg',
                'location': 'Yala Buffer Wilderness',
                'credit': 'Eco-Luxury Camp'
            },
            {
                'title': 'Alfresco Kumbuk Bush Dining',
                'category': 'camp',
                'image': 'images/jungle-cuisine.jpg',
                'location': 'Manik River Bank',
                'credit': 'Wilderness Culinary Desk'
            },
            {
                'title': 'Sri Lankan Sloth Bear in Summer Palu Season',
                'category': 'photo',
                'image': 'images/yala-wildlife-hero.jpg',
                'location': 'Yala Block 5 Corridor',
                'credit': 'Photo by Sahan W.'
            },
            {
                'title': 'High-Performance Safari Land Cruiser',
                'category': 'drives',
                'image': 'images/hero-safari-jeep.jpg',
                'location': 'Wickrama Desk Desk',
                'credit': '4x4 Expedition Fleet'
            }
        ],
        'review_success': review_success
    }
    return render(request, 'core/reviews.html', context)

def tickets(request):

    ticket_success = None
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        country = request.POST.get('country', '').strip()
        email = request.POST.get('email_address', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        ticket_date = request.POST.get('ticket_date', '').strip()
        message = request.POST.get('message', '').strip()

        try:
            foreign_adults = int(request.POST.get('foreign_adults', 1))
            foreign_children = int(request.POST.get('foreign_children', 0))
            saarc_adults = int(request.POST.get('saarc_adults', 0))
            saarc_children = int(request.POST.get('saarc_children', 0))
            local_adults = int(request.POST.get('local_adults', 0))
            local_children = int(request.POST.get('local_children', 0))
            infants = int(request.POST.get('infants', 0))

            jeeps = int(request.POST.get('jeeps', 1))
            cars = int(request.POST.get('cars', 0))
            buses = int(request.POST.get('buses', 0))
        except (ValueError, TypeError):
            foreign_adults, foreign_children = 1, 0
            saarc_adults, saarc_children = 0, 0
            local_adults, local_children, infants = 0, 0, 0
            jeeps, cars, buses = 1, 0, 0

        try:
            entry_fees_lkr = float(request.POST.get('entry_fees_lkr', 0))
            vehicle_fees_lkr = float(request.POST.get('vehicle_fees_lkr', 0))
            service_fee_lkr = float(request.POST.get('service_fee_lkr', 0))
            subtotal_lkr = float(request.POST.get('subtotal_lkr', 0))
            vat_lkr = float(request.POST.get('vat_lkr', 0))
            gateway_fee_lkr = float(request.POST.get('gateway_fee_lkr', 0))
            total_lkr = float(request.POST.get('calculated_total_lkr', 0))
            total_usd = float(request.POST.get('calculated_total_usd', 0))
        except (ValueError, TypeError):
            entry_fees_lkr = vehicle_fees_lkr = service_fee_lkr = subtotal_lkr = vat_lkr = gateway_fee_lkr = total_lkr = total_usd = 0.0

        import time
        ref_code = f"PR-{int(time.time())}"

        def _async_send_permit_emails():
            try:
                from django.core.mail import EmailMultiAlternatives
                from django.conf import settings

                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Yala Leopard Tracks <yalaleopardtracks@gmail.com>')

                breakdown_items = ""
                if foreign_adults > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Foreign Adults ($25 USD)</td><td style='padding: 8px 12px; text-align: right;'>{foreign_adults}</td></tr>"
                if foreign_children > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Foreign Children ($15 USD)</td><td style='padding: 8px 12px; text-align: right;'>{foreign_children}</td></tr>"
                if saarc_adults > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>SAARC Adults ($20 USD)</td><td style='padding: 8px 12px; text-align: right;'>{saarc_adults}</td></tr>"
                if saarc_children > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>SAARC Children ($10 USD)</td><td style='padding: 8px 12px; text-align: right;'>{saarc_children}</td></tr>"
                if local_adults > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Local Adults (LKR 150)</td><td style='padding: 8px 12px; text-align: right;'>{local_adults}</td></tr>"
                if local_children > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Local Children (LKR 100)</td><td style='padding: 8px 12px; text-align: right;'>{local_children}</td></tr>"
                if infants > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Infants (Free)</td><td style='padding: 8px 12px; text-align: right;'>{infants}</td></tr>"
                if jeeps > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Safari Jeeps / Vans</td><td style='padding: 8px 12px; text-align: right;'>{jeeps}</td></tr>"
                if cars > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Cars / SUVs</td><td style='padding: 8px 12px; text-align: right;'>{cars}</td></tr>"
                if buses > 0:
                    breakdown_items += f"<tr style='border-bottom: 1px dashed #E5E5E5;'><td style='padding: 8px 12px;'>Buses / Lorries</td><td style='padding: 8px 12px; text-align: right;'>{buses}</td></tr>"

                breakdown_html = f"""
                <table style="width: 100%; border-collapse: collapse; margin-top: 14px; font-size: 14px; color: #233325; background: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid rgba(96,108,56,0.2);">
                    <tr style="background: #FAF6EE; border-bottom: 1px solid rgba(96,108,56,0.2);">
                        <td style="padding: 10px 12px; font-weight: 700;">Passenger & Vehicle Items</td>
                        <td style="padding: 10px 12px; text-align: right; font-weight: 700;">Quantity</td>
                    </tr>
                    {breakdown_items}
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 14px; color: #233325; background: #FFFFFF; border-radius: 12px; overflow: hidden; border: 1px solid rgba(96,108,56,0.2);">
                    <tr style="border-bottom: 1px solid #F0F0F0;"><td style="padding: 10px 14px; color: #666;">Entry Fees Subtotal</td><td style="padding: 10px 14px; text-align: right; font-weight: 600;">LKR {entry_fees_lkr:,.2f}</td></tr>
                    <tr style="border-bottom: 1px solid #F0F0F0;"><td style="padding: 10px 14px; color: #666;">Vehicle Admission Fees</td><td style="padding: 10px 14px; text-align: right; font-weight: 600;">LKR {vehicle_fees_lkr:,.2f}</td></tr>
                    <tr style="border-bottom: 1px solid #F0F0F0;"><td style="padding: 10px 14px; color: #666;">Mandatory DWC Service Fee</td><td style="padding: 10px 14px; text-align: right; font-weight: 600;">LKR {service_fee_lkr:,.2f}</td></tr>
                    <tr style="border-bottom: 1px solid #F0F0F0; font-weight: 700; background: rgba(96,108,56,0.05);"><td style="padding: 10px 14px;">Subtotal</td><td style="padding: 10px 14px; text-align: right;">LKR {subtotal_lkr:,.2f}</td></tr>
                    <tr style="border-bottom: 1px solid #F0F0F0;"><td style="padding: 10px 14px; color: #666;">Government VAT (18%)</td><td style="padding: 10px 14px; text-align: right; font-weight: 600;">LKR {vat_lkr:,.2f}</td></tr>
                    <tr style="border-bottom: 1px solid #F0F0F0;"><td style="padding: 10px 14px; color: #666;">Gateway Processing (2%)</td><td style="padding: 10px 14px; text-align: right; font-weight: 600;">LKR {gateway_fee_lkr:,.2f}</td></tr>
                    <tr style="background: #606C38; color: #FFFFFF; font-weight: 800; font-size: 16px;">
                        <td style="padding: 14px;">Total Estimated Cost</td>
                        <td style="padding: 14px; text-align: right;">LKR {total_lkr:,.2f} (~ ${total_usd:.2f} USD)</td>
                    </tr>
                </table>
                """

                guest_subject = f"Yala Park Entrance Permit Request Confirmation - Ref #{ref_code}"
                guest_text = f"Dear {full_name},\n\nThank you for requesting official Yala National Park entrance permits with Yala Leopard Tracks.\n\nSafari Date: {ticket_date}\nTotal Cost: LKR {total_lkr:,.2f} (~ ${total_usd:.2f} USD)\nReference ID: #{ref_code}\n\nOur expedition desk will process your express gate voucher shortly."
                
                guest_html = f"""
                <div style="background-color: #FAF6EE; padding: 24px 12px; font-family: 'Inter', Helvetica, Arial, sans-serif;">
                    <div style="max-width: 620px; margin: 0 auto; background: #FFFFFF; border-radius: 24px; overflow: hidden; border: 1px solid rgba(71, 81, 40, 0.18);">
                        <div style="background-color: #122118; padding: 32px 24px; text-align: center; color: #FFFFFF; border-bottom: 3px solid #D4AF37;">
                            <h1 style="font-size: 22px; font-weight: 800; letter-spacing: 1px; margin: 0; color: #FAF6EE;">YALA LEOPARD TRACKS</h1>
                            <p style="font-size: 13px; color: #D4AF37; margin: 6px 0 0 0; font-weight: 600; text-transform: uppercase;">Official DWC Park Entrance Permit Confirmation</p>
                        </div>
                        <div style="padding: 30px 24px; background-color: #FAF6EE;">
                            <h2 style="color: #233325; font-size: 18px; font-weight: 800; margin-top: 0;">Permit Reservation Request Received!</h2>
                            <p style="color: #4A5568; font-size: 14px; line-height: 1.6;">
                                Dear <strong>{full_name}</strong>,<br>
                                Thank you for submitting your Yala National Park entrance permit request. Below is your detailed breakdown of official DWC entrance fees, vehicle trail charges, and government taxes.
                            </p>
                            
                            <div style="background: #FFFFFF; border-radius: 16px; padding: 20px; border: 1px solid rgba(96,108,56,0.2); margin-bottom: 20px;">
                                <div style="font-size: 14px; margin-bottom: 8px;"><strong>Permit Reference:</strong> #{ref_code}</div>
                                <div style="font-size: 14px; margin-bottom: 8px;"><strong>Safari Date:</strong> {ticket_date}</div>
                                <div style="font-size: 14px; margin-bottom: 8px;"><strong>Guest Name:</strong> {full_name} ({country})</div>
                                <div style="font-size: 14px; margin-bottom: 8px;"><strong>Phone / WhatsApp:</strong> {phone_number}</div>
                                {f'<div style="font-size: 14px; margin-bottom: 8px;"><strong>Special Request:</strong> {message}</div>' if message else ''}
                            </div>

                            <h3 style="color: #233325; font-size: 16px; font-weight: 800; margin-bottom: 8px;">Detailed Tariff & Tax Breakdown</h3>
                            {breakdown_html}

                            <div style="margin-top: 24px; background: rgba(96,108,56,0.08); padding: 16px; border-radius: 12px; font-size: 13px; color: #233325; line-height: 1.6;">
                                📌 <strong>Next Steps:</strong> Our safari coordination team will review your permit request and issue your express park entry vouchers. If you have reserved safari jeep transportation with us, your driver will hold physical tickets at the Palatupana gate desk.
                            </div>
                        </div>
                        <div style="background-color: #122118; padding: 24px; text-align: center; font-size: 12px; color: #999999;">
                            <p style="margin: 0;">Yala Leopard Tracks • Tissamaharama / Yala National Park, Sri Lanka</p>
                            <p style="margin: 4px 0 0 0;">Email: <a href="mailto:yalaleopardtracks@gmail.com" style="color: #D4AF37; text-decoration: none;">yalaleopardtracks@gmail.com</a> | WhatsApp: +94 77 815 8004</p>
                        </div>
                    </div>
                </div>
                """

                msg_guest = EmailMultiAlternatives(guest_subject, guest_text, from_email, [email])
                msg_guest.attach_alternative(guest_html, "text/html")
                msg_guest.send(fail_silently=True)

                # Send 1 Email to Admin / Our Desk to Show Bookings
                admin_subject = f"NEW TICKET PERMIT BOOKING: #{ref_code} - {full_name} ({ticket_date})"
                admin_text = f"New Park Permit Booking Request:\nRef: #{ref_code}\nName: {full_name}\nCountry: {country}\nEmail: {email}\nPhone: {phone_number}\nDate: {ticket_date}\nTotal Cost: LKR {total_lkr:,.2f} (~ ${total_usd:.2f} USD)"
                admin_recipients = ['yalaleopardtracks@gmail.com', 'pasinduwickramasooriya@gmail.com']

                msg_admin = EmailMultiAlternatives(admin_subject, admin_text, from_email, admin_recipients)
                msg_admin.attach_alternative(guest_html, "text/html")
                msg_admin.send(fail_silently=True)

            except Exception as mail_err:
                print('TICKET_PERMIT_EMAIL_ERROR:', str(mail_err))


        import threading
        threading.Thread(target=_async_send_permit_emails, daemon=True).start()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'status': 'success',
                'message': f'Thank you, {full_name}! Your Yala park entrance permit reservation request has been submitted successfully. A confirmation email with the complete price breakdown has been sent to {email}.',
                'ref_code': ref_code
            })

        ticket_success = f"Thank you, {full_name}! Your Yala park entrance permit reservation request has been received. Express queue vouchers and price breakdown confirmation have been emailed to {email}."


    context = {
        'title': 'Yala National Park Tickets & Entrance Fees | Yala Leopard Tracks',
        'ticket_rates': [
            {
                'id': 'foreign-adult',
                'title': 'Foreign Adult Ticket',
                'price_usd': '$40 USD',
                'price_lkr': 'Approx Rs. 12,800 LKR',
                'age_limit': 'Ages 12+',
                'inclusions': [
                    'National Park Entry Permit',
                    'Department of Wildlife Conservation Fee',
                    'DWC Service Tax & 15% VAT Included',
                    'Express Gate Queue-Jump Voucher'
                ],
                'popular': True
            },
            {
                'id': 'foreign-child',
                'title': 'Foreign Child Ticket',
                'price_usd': '$20 USD',
                'price_lkr': 'Approx Rs. 6,400 LKR',
                'age_limit': 'Ages 6 - 11 (Under 6 FREE)',
                'inclusions': [
                    'Child National Park Permit',
                    'All DWC Taxes & Fees Included',
                    'Free Educational Animal Chart'
                ],
                'popular': False
            },
            {
                'id': 'jeep-permit-tariff',
                'title': 'Private 4x4 Jeep Tariff',
                'price_usd': '$15 USD',
                'price_lkr': 'Approx Rs. 4,800 LKR',
                'age_limit': 'Per 4x4 Vehicle Entry',
                'inclusions': [
                    'Jeep Entrance License Fee',
                    'Park Gate Vehicle Registration',
                    'Licensed Naturalist Tracker Entry'
                ],
                'popular': True
            },
            {
                'id': 'local-resident',
                'title': 'Sri Lankan Citizen Ticket',
                'price_usd': 'Rs. 350 LKR',
                'price_lkr': 'Child: Rs. 150 LKR',
                'age_limit': 'NIC / Passport Holders',
                'inclusions': [
                    'Resident Park Entrance Ticket',
                    'DWC Conservation Tax'
                ],
                'popular': False
            }
        ],
        'gates_info': [
            {
                'name': 'Palatupana Gate (Block 1 Main Gate)',
                'hours': '06:00 AM – 06:00 PM',
                'location': 'Southern Entrance (Near Tissamaharama / Kirinda)',
                'description': 'The primary entrance for Yala Block 1 with the highest density of Sri Lankan leopards and sloth bears.'
            },
            {
                'name': 'Katagamuwa Gate (Block 1 & 2 Gate)',
                'hours': '06:00 AM – 06:00 PM',
                'location': 'Kataragama Entrance (Near Sacred City)',
                'description': 'Alternative entrance with shorter queue times, ideal for guests staying in Kataragama.'
            },
            {
                'name': 'Galge Gate (Block 3, 4 & 5 Gate)',
                'hours': '06:00 AM – 06:00 PM',
                'location': 'Northern Entrance (Büttala - Kataragama Road)',
                'description': 'Quiet, uncrowded park block famous for wild elephant herds and birdwatching waterholes.'
            }
        ],
        'ticket_success': ticket_success
    }
    return render(request, 'core/tickets.html', context)


def policies(request):
    """
    Legal Policies View: Consolidates Privacy Policy, Terms of Service, and Refund Policy.
    """
    context = {
        'title': 'Privacy Policy, Terms of Service & Refund Policy | Yala Leopard Tracks',
    }
    return render(request, 'core/policies.html', context)


def robots_txt(request):
    """
    Returns robots.txt for Googlebot and search engines.
    """
    from django.http import HttpResponse
    content = """User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {}://{}/sitemap.xml
""".format(request.scheme, request.get_host())
    return HttpResponse(content, content_type="text/plain")


def site_webmanifest(request):
    """
    Returns site.webmanifest for PWA & Google Search logo indexing.
    """
    from django.http import JsonResponse
    data = {
        "name": "Yala Leopard Tracks",
        "short_name": "LeopardTracks",
        "icons": [
            {
                "src": f"{request.scheme}://{request.get_host()}/static/images/favicon.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": f"{request.scheme}://{request.get_host()}/static/images/logo-official.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "theme_color": "#606C38",
        "background_color": "#FAF6EE",
        "display": "standalone"
    }
    return JsonResponse(data)


def sitemap_xml(request):
    """
    Dynamically generates sitemap.xml listing all static pages and dynamic model pages.
    """
    from django.http import HttpResponse
    from django.urls import reverse
    from xml.sax.saxutils import escape

    domain = f"{request.scheme}://{request.get_host()}"
    
    # 1. Core Static Pages
    static_urls = [
        {'loc': domain + '/', 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': domain + reverse('packages'), 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': domain + reverse('tours'), 'changefreq': 'daily', 'priority': '0.9'},
        {'loc': domain + reverse('tickets'), 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': domain + reverse('blog'), 'changefreq': 'daily', 'priority': '0.8'},
        {'loc': domain + reverse('about'), 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': domain + reverse('contact'), 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': domain + reverse('reviews'), 'changefreq': 'weekly', 'priority': '0.7'},
        {'loc': domain + reverse('policies'), 'changefreq': 'monthly', 'priority': '0.5'},
    ]

    xml_entries = []
    for item in static_urls:
        xml_entries.append(f"""  <url>
    <loc>{escape(item['loc'])}</loc>
    <changefreq>{item['changefreq']}</changefreq>
    <priority>{item['priority']}</priority>
  </url>""")

    # 2. Dynamic Safari Packages
    for pkg in SafariPackage.objects.all():
        if pkg.slug:
            try:
                url = f"{domain}{reverse('package_detail', kwargs={'slug': pkg.slug})}"
                xml_entries.append(f"""  <url>
    <loc>{escape(url)}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")
            except Exception:
                pass

    # 3. Dynamic Tours
    for tr in Tour.objects.all():
        if tr.slug:
            try:
                url = f"{domain}{reverse('tour_detail', kwargs={'slug': tr.slug})}"
                xml_entries.append(f"""  <url>
    <loc>{escape(url)}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")
            except Exception:
                pass

    # 4. Dynamic Blog Posts
    for post in BlogPost.objects.all():
        if post.slug:
            try:
                url = f"{domain}{reverse('blog_detail', kwargs={'slug': post.slug})}"
                lastmod = post.updated_at.strftime('%Y-%m-%d') if getattr(post, 'updated_at', None) else (post.created_at.strftime('%Y-%m-%d') if getattr(post, 'created_at', None) else '')
                lastmod_tag = f"\n    <lastmod>{lastmod}</lastmod>" if lastmod else ""
                xml_entries.append(f"""  <url>
    <loc>{escape(url)}</loc>{lastmod_tag}
    <changefreq>weekly</changefreq>
    <priority>0.80</priority>
  </url>""")
            except Exception:
                pass

    joined_entries = "\n".join(xml_entries)
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{joined_entries}
</urlset>"""

    return HttpResponse(xml_content, content_type="application/xml")













