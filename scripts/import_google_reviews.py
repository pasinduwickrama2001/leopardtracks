#!/usr/bin/env python
"""
Google Maps Review Scraper & Importer for Yala Leopard Tracks (Django)
=============================================================================
Scrapes real reviews, ratings, reviewer avatars, and high-resolution photo URLs
directly from Google Maps place URLs using Playwright, and imports them into
the Django GuestReview database.
"""

import os
import sys
import re
import time
import json
import argparse

# Initialize Django Environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from core.models import GuestReview
from django.db import transaction

DEFAULT_GOOGLE_MAPS_URL = (
    "https://www.google.com/maps/place/Yala+National+Park/@6.4639613,81.4693098,17z/data="
    "!4m8!3m7!1s0x3ae5d3a62ffb9359:0x3bb623d70b5a3314!8m2!3d6.4639613!4d81.4718847"
    "!9m1!1b1!16zL20vMDJxMXo1?entry=ttu&g_ep=EgoyMDI2MDkxNS4wIKXMDSoASAFQAw%3D%3D"
)

DEFAULT_JSON_PATH = os.path.join(BASE_DIR, 'scripts', 'data', 'google_reviews.json')
FALLBACK_JSON_PATH = '/Users/pasinduwickramasuriya/Documents/GitHub/yala-wildlife/data/review-photos.json'


def categorize_review(text, has_photo=False):
    """Categorizes reviews into model categories based on content keywords."""
    lower = text.lower()
    if any(k in lower for k in ['camp', 'tent', 'glamping', 'stay', 'lodge', 'cabin', 'bungalow', 'resort']):
        return 'camp'
    elif any(k in lower for k in ['photo', 'camera', 'lens', 'photograph', 'capture', 'shot', 'dslr']):
        return 'photo'
    elif any(k in lower for k in ['leopard', 'panther', 'cub', 'cat', 'predator', 'spotted']):
        return 'leopard'
    elif any(k in lower for k in ['safari', 'game drive', 'driver', 'guide', 'jeep', 'tracker', 'tour', 'park', 'elephant', 'bear']):
        return 'drives'
    return 'leopard' if has_photo else 'drives'


def scrape_google_maps_reviews(url, max_scrolls=150, limit=1000, sort_newest=True, headless=True):
    """
    Automates Chromium via Playwright to fetch reviews from Google Maps.
    Extracts author name, avatar, rating, relative date, full text, and high-res photos.
    """
    from playwright.sync_api import sync_playwright

    print("==========================================================================")
    print("🚀 STARTING GOOGLE MAPS REVIEW EXTRACTION ENGINE")
    print(f"🔗 Target URL: {url}")
    print(f"🎯 Max Scrolls: {max_scrolls} | Target Limit: {limit}")
    print(f"🔀 Sort by Newest: {sort_newest} | Headless: {headless}")
    print("==========================================================================")

    scraped_reviews = []
    seen_review_ids = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--lang=en-US']
        )
        context = browser.new_context(
            viewport={'width': 1400, 'height': 1200},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US'
        )
        # Pre-set Google consent cookies so Google does not display cookie dialog
        context.add_cookies([
            {'name': 'SOCS', 'value': 'CAESHAgBEhJnd3NfMjAyMzAzMjItMF9SQzEaAmRlIAEaBgiAo_CmBg', 'domain': '.google.com', 'path': '/'},
            {'name': 'CONSENT', 'value': 'YES+cb.20230531-04-p0.en+FX+917', 'domain': '.google.com', 'path': '/'}
        ])

        page = context.new_page()

        print("🗺️ Navigating to Google Maps...")
        page.goto(url, wait_until='domcontentloaded', timeout=45000)
        time.sleep(3)

        # Handle cookie consent button if present
        try:
            consent_btn = page.query_selector(
                'button[aria-label*="Accept all" i], button:has-text("Accept all"), button:has-text("I agree")'
            )
            if consent_btn:
                consent_btn.click()
                print("🍪 Handled cookie consent dialog.")
                time.sleep(2)
        except Exception:
            pass

        # Ensure Reviews tab is selected
        try:
            page.wait_for_selector('div[data-review-id]', timeout=6000)
            print("✅ Reviews container active directly.")
        except Exception:
            print("ℹ️ Waiting for reviews or clicking Reviews tab...")
            reviews_tab = page.query_selector('button[aria-label*="Reviews" i], div[role="tab"][aria-label*="Reviews" i]')
            if reviews_tab:
                reviews_tab.click()
                time.sleep(2)
            page.wait_for_selector('div[data-review-id]', timeout=15000)

        # Optional sort by Newest to reveal the freshest reviews
        if sort_newest:
            try:
                sort_btn = page.query_selector('button[aria-label*="Sort" i]')
                if sort_btn:
                    sort_btn.click()
                    time.sleep(1.5)
                    menu_items = page.query_selector_all('div[role="menuitemradio"]')
                    if len(menu_items) > 1:
                        menu_items[1].click()
                        print("🔀 Sorted reviews by 'Newest'.")
                        time.sleep(4)
            except Exception as e:
                print(f"⚠️ Sort toggle notice: {e}")

        # Hover over the reviews pane to focus scrolling
        try:
            page.hover('div[role="main"] div[tabindex="-1"]')
        except Exception:
            page.mouse.move(250, 400)

        no_new_data_count = 0
        last_extracted_count = 0

        for scroll_idx in range(1, max_scrolls + 1):
            # 1. Expand "See more" buttons for truncated reviews
            try:
                page.evaluate('''() => {
                    const moreBtns = document.querySelectorAll('button[aria-label*="See more" i], button.w8nwRe');
                    for (const btn of moreBtns) {
                        try { btn.click(); } catch(e) {}
                    }
                }''')
            except Exception:
                pass

            # 2. Extract visible reviews from DOM
            batch = page.evaluate('''() => {
                const cards = Array.from(document.querySelectorAll('div[data-review-id]'));
                return cards.map(card => {
                    const reviewId = card.getAttribute('data-review-id') || '';
                    const authorEl = card.querySelector('.d4r55');
                    const author = (authorEl ? authorEl.textContent : card.getAttribute('aria-label') || '').trim();

                    const starsEl = card.querySelector('[aria-label*="star" i], span.kvMYJc');
                    let rating = 5;
                    if (starsEl) {
                        const aria = starsEl.getAttribute('aria-label') || '';
                        const m = aria.match(/\\d+/);
                        if (m) rating = parseInt(m[0]);
                    }

                    const timeEl = card.querySelector('.rsqaWe, .xuAUBe');
                    const relTime = timeEl ? timeEl.textContent.trim() : '';

                    const textEl = card.querySelector('.wiI7pd');
                    const text = textEl ? textEl.textContent.trim() : '';

                    // Avatar URL
                    const avatarImg = card.querySelector('button img, img.NBa7we');
                    const avatarUrl = avatarImg ? (avatarImg.src || '') : '';

                    // Photos (high-resolution upgrade: =w1200-h900)
                    let photoUrl = '';
                    const btnPhotos = Array.from(card.querySelectorAll('button[style*="background-image"]'));
                    for (const bp of btnPhotos) {
                        const style = bp.getAttribute('style') || '';
                        const m = style.match(/url\\([\"\\']?(https?[^\"\\')]+)/);
                        if (m) {
                            photoUrl = m[1].replace(/=w\\d+-h\\d+.*$/, '=w1200-h900').replace(/=s\\d+.*$/, '=s1200');
                            break;
                        }
                    }
                    if (!photoUrl) {
                        const imgs = Array.from(card.querySelectorAll('img[src*="googleusercontent.com"]'));
                        for (const img of imgs) {
                            const src = img.src || '';
                            if (src.includes('=w36') || src.includes('=w48') || src.includes('=w100') || src.includes('-p-rp') || src.includes('br100')) continue;
                            photoUrl = src.replace(/=w\\d+-h\\d+.*$/, '=w1200-h900').replace(/=s\\d+.*$/, '=s1200');
                            break;
                        }
                    }

                    return {
                        id: reviewId,
                        author: author || 'Google Maps Reviewer',
                        rating: rating,
                        date: relTime || 'Recent',
                        text: text,
                        avatar_url: avatarUrl,
                        photo_url: photoUrl
                    };
                });
            }''')

            added_this_loop = 0
            for item in batch:
                rid = item.get('id', '').strip()
                author = item.get('author', '').strip()
                text = item.get('text', '').strip()
                unique_key = rid if rid else f"{author}_{text[:40]}"

                if unique_key not in seen_review_ids:
                    seen_review_ids.add(unique_key)
                    scraped_reviews.append(item)
                    added_this_loop += 1

            current_total = len(scraped_reviews)
            print(f"   Scroll {scroll_idx}/{max_scrolls}: {len(batch)} cards in DOM | +{added_this_loop} new | Total Collected: {current_total}")

            if current_total >= limit:
                print(f"🎯 Target limit of {limit} reviews reached!")
                break

            if current_total == last_extracted_count:
                no_new_data_count += 1
                if no_new_data_count >= 8:
                    print("⏹️ No new reviews loaded after 8 consecutive scrolls. Stream ended.")
                    break
            else:
                no_new_data_count = 0

            last_extracted_count = current_total

            # 3. Robust scroll down using combined DOM scrollTop + scrollIntoView + wheel event
            page.evaluate('''() => {
                const cards = Array.from(document.querySelectorAll('div[data-review-id]'));
                if (cards.length > 0) {
                    cards[cards.length - 1].scrollIntoView({ behavior: 'auto', block: 'end' });
                }
                const scrollContainers = Array.from(document.querySelectorAll('.m6QErb[aria-label]'));
                for (let el of scrollContainers) {
                    if (el.scrollHeight > el.clientHeight) {
                        el.scrollTop = el.scrollHeight;
                    }
                }
            }''')
            page.mouse.move(250, 400)
            page.mouse.wheel(0, 3000)
            time.sleep(3.5)

        browser.close()

    print(f"\n🎉 Successfully scraped {len(scraped_reviews)} unique reviews from Google Maps!")
    return scraped_reviews


def save_scraped_data(reviews, json_path):
    """Saves scraped reviews list into a formatted JSON file."""
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved {len(reviews)} reviews to: {json_path}")


def load_reviews_from_file(json_path):
    """Loads reviews from a previously scraped JSON file."""
    if not os.path.exists(json_path):
        if os.path.exists(FALLBACK_JSON_PATH):
            json_path = FALLBACK_JSON_PATH
        else:
            print(f"❌ ERROR: JSON file not found at {json_path}")
            return []

    print(f"📂 Loading reviews from: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Normalize format if loaded from old review-photos.json format
    normalized = []
    for item in data:
        author = item.get('author') or item.get('authorName') or 'Google Maps Reviewer'
        text = item.get('text') or item.get('reviewText') or ''
        rating = item.get('rating', 5)
        date_str = item.get('date') or item.get('relativeTime') or 'Recent'
        photo = item.get('photo_url') or item.get('url') or ''
        avatar = item.get('avatar_url', '')

        normalized.append({
            'author': author.strip(),
            'rating': rating,
            'date': date_str.strip(),
            'text': text.strip(),
            'avatar_url': avatar.strip(),
            'photo_url': photo.strip()
        })

    return normalized


def import_to_database(reviews_data, limit=6000):
    """
    Inserts scraped/loaded reviews into Django GuestReview database.
    Deduplicates against existing records and assigns categories & packages.
    """
    print("\n==========================================================================")
    print("📍 YALA LEOPARD TRACKS - DATABASE IMPORT ENGINE")
    print(f"🎯 IMPORT LIMIT: UP TO {limit} REVIEWS")
    print("==========================================================================")

    # Deduplicate within input
    unique_map = {}
    for item in reviews_data:
        author = item.get('author', 'Google Reviewer').strip()
        text = item.get('text', '').strip()
        rating = item.get('rating', 5)
        date_val = item.get('date', 'Recent').strip()
        photo = item.get('photo_url', '').strip()
        avatar = item.get('avatar_url', '').strip()

        key = f"{author}_{text[:50]}"
        if key not in unique_map:
            category = categorize_review(text, has_photo=bool(photo))
            unique_map[key] = {
                'name': author if author else 'Google Reviewer',
                'origin': 'Google Maps Verified Reviewer',
                'date': date_val if date_val else 'Recent',
                'package': 'Yala National Park Safari Drive',
                'rating': rating if 1 <= rating <= 5 else 5,
                'comment': text if text else 'Breathtaking safari experience in Yala National Park!',
                'photo_url': photo,
                'avatar_url': avatar,
                'category': category,
                'source': 'Google Maps',
                'verified': True
            }

    candidate_list = list(unique_map.values())[:limit]
    print(f"✨ Prepared {len(candidate_list)} unique candidate reviews for database.")

    # Check existing keys in DB to avoid duplicate insertion
    existing_keys = set(GuestReview.objects.values_list('name', 'comment'))

    new_objects = []
    for item in candidate_list:
        comment_val = item['comment']
        name_val = item['name']
        if (name_val, comment_val) not in existing_keys:
            new_objects.append(
                GuestReview(
                    name=name_val,
                    origin=item['origin'],
                    date=item['date'],
                    package=item['package'],
                    rating=item['rating'],
                    comment=comment_val,
                    verified=item['verified'],
                    avatar_url=item['avatar_url'],
                    photo_url=item['photo_url'],
                    source=item['source'],
                    category=item['category']
                )
            )

    print(f"⚡ BULK INSERTING {len(new_objects)} NEW GOOGLE MAPS REVIEWS INTO DATABASE...")

    if new_objects:
        with transaction.atomic():
            GuestReview.objects.bulk_create(new_objects, batch_size=500)

    total_in_db = GuestReview.objects.count()
    reviews_with_photos = GuestReview.objects.exclude(photo_url='').exclude(photo_url__isnull=True).count()
    reviews_with_avatars = GuestReview.objects.exclude(avatar_url='').exclude(avatar_url__isnull=True).count()

    print("--------------------------------------------------------------------------")
    print("🎉 GOOGLE MAPS REVIEWS IMPORT COMPLETED!")
    print(f"   - Input Candidate Reviews:        {len(candidate_list)}")
    print(f"   - New Reviews Added to Database:  {len(new_objects)}")
    print(f"   - Already Existing Skipped:       {len(candidate_list) - len(new_objects)}")
    print(f"   - TOTAL ACTIVE REVIEWS IN DB:     {total_in_db}")
    print(f"   - REVIEWS WITH HIGH-RES PHOTOS:   {reviews_with_photos}")
    print(f"   - REVIEWS WITH AVATARS:           {reviews_with_avatars}")
    print("==========================================================================")


def main():
    parser = argparse.ArgumentParser(description="Google Maps Review Scraper and Django Importer")
    parser.add_argument(
        '--url',
        type=str,
        default=DEFAULT_GOOGLE_MAPS_URL,
        help="Google Maps Place URL to scrape reviews from"
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=500,
        help="Maximum number of reviews to extract/import (default: 500)"
    )
    parser.add_argument(
        '--max-scrolls',
        type=int,
        default=60,
        help="Maximum scroll iterations on Google Maps (default: 60)"
    )
    parser.add_argument(
        '--json-path',
        type=str,
        default=DEFAULT_JSON_PATH,
        help="Path to save or read reviews JSON file"
    )
    parser.add_argument(
        '--import-only',
        action='store_true',
        help="Skip live scraping and import existing reviews from JSON file"
    )
    parser.add_argument(
        '--scrape-only',
        action='store_true',
        help="Only scrape and save to JSON, do not import into Django database"
    )
    parser.add_argument(
        '--headed',
        action='store_true',
        help="Run browser in visible mode (default is headless)"
    )
    parser.add_argument(
        '--no-sort',
        action='store_true',
        help="Do not sort by newest (keep Google Maps default relevance sorting)"
    )
    args = parser.parse_args()

    if args.import_only:
        reviews = load_reviews_from_file(args.json_path)
    else:
        reviews = scrape_google_maps_reviews(
            url=args.url,
            max_scrolls=args.max_scrolls,
            limit=args.limit,
            sort_newest=not args.no_sort,
            headless=not args.headed
        )
        if reviews:
            save_scraped_data(reviews, args.json_path)

    if not args.scrape_only and reviews:
        import_to_database(reviews, limit=args.limit)


if __name__ == '__main__':
    main()

