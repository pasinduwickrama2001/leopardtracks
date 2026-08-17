from django.shortcuts import render

def home(request):
    context = {
        'title': 'Yala Leopard Tracks | Yala National Park Safaris & Luxury Camping Sri Lanka',
        'featured_trails': [
            {'name': 'Yala Block 1 Safari', 'duration': '3 Hours', 'tag': 'Popular'},
            {'name': 'Kumana Bird Sanctuary Trail', 'duration': '4 Hours', 'tag': 'Scenic'},
            {'name': 'Lunugamvehera Wildlife Corridor', 'duration': '5 Hours', 'tag': 'Adventure'},
        ]
    }
    return render(request, 'core/home.html', context)

def packages(request):
    context = {
        'title': 'Yala Safari Packages & Expeditions | Yala Leopard Tracks',
        'packages_list': [
            {
                'id': 'yala-morning-leopard',
                'category': 'half-day',
                'category_label': 'HALF-DAY GAME DRIVE',
                'tag_class': 'tag-sage',
                'title': 'Yala Block 1 Morning Leopard Game Drive',
                'subtitle': 'Prime early morning tracking when leopards and sloth bears are most active.',
                'price': '$120',
                'price_unit': 'per 4x4 jeep (up to 6 guests)',
                'duration': '5 Hours (05:30 AM – 10:30 AM)',
                'vehicle': 'Private Modified Toyota Land Cruiser 4x4',
                'inclusions': [
                    'Licensed Senior Naturalist Tracker',
                    'Official National Park Entry Permits',
                    'Chilled Bottled Mineral Water & Juices',
                    'Fresh Tropical Fruit Basket',
                    'Binoculars & Dust Goggles'
                ],
                'highlights': 'High probability leopard tracking in Block 1, sloth bear sightings, coastal lagoon birding.',
                'featured': True
            },
            {
                'id': 'yala-full-day-expedition',
                'category': 'full-day',
                'category_label': 'FULL-DAY EXPEDITION',
                'tag_class': 'tag-amber',
                'title': 'Yala Full-Day Deep Wilderness Expedition',
                'subtitle': 'Comprehensive 12-hour deep park exploration spanning Block 1 and Block 5.',
                'price': '$240',
                'price_unit': 'per 4x4 jeep (up to 6 guests)',
                'duration': '12 Hours (05:30 AM – 06:00 PM)',
                'vehicle': 'Heavy-Duty 4x4 Land Cruiser with USB Charging Ports',
                'inclusions': [
                    'Master Wildlife Naturalist Tracker',
                    'Full-Day National Park Permits & Taxes',
                    'Gourmet Breakfast Picnic by Manik River',
                    'Traditional Sri Lankan Jungle Lunch BBQ',
                    'All Day Chilled Refreshments & Snacks'
                ],
                'highlights': 'Deep Block 1 & 5 exploration, elephant herds, sloth bears, leopard territory tracking.',
                'featured': True
            },
            {
                'id': 'yala-sunset-safari',
                'category': 'half-day',
                'category_label': 'AFTERNOON GAME DRIVE',
                'tag_class': 'tag-terracotta',
                'title': 'Yala Block 5 & Manik River Sunset Safari',
                'subtitle': 'Golden hour game drive focusing on watering holes and riverfront wildlife.',
                'price': '$110',
                'price_unit': 'per 4x4 jeep (up to 6 guests)',
                'duration': '4 Hours (02:30 PM – 06:30 PM)',
                'vehicle': 'Elevated Open-Air 4x4 Safari Jeep',
                'inclusions': [
                    'Experienced Wildlife Tracker',
                    'National Park Entrance Permits',
                    'Riverfront Ceylon Tea & Spiced Snacks',
                    'Cold Towels & Mineral Water'
                ],
                'highlights': 'Scenic Manik River banks, mugger crocodiles, peacocks, sunset golden hour photography.',
                'featured': False
            },
            {
                'id': 'yala-luxury-camp-package',
                'category': 'luxury-camp',
                'category_label': 'LUXURY TENTED CAMP PACKAGE',
                'tag_class': 'tag-rose',
                'title': '2-Day Luxury Tented Camp & Dual Safari Package',
                'subtitle': 'All-inclusive wilderness glamping with morning and afternoon game drives.',
                'price': '$450',
                'price_unit': 'per person (all-inclusive)',
                'duration': '2 Days / 1 Night Stay',
                'vehicle': 'Luxury Private 4x4 Game Viewing Jeep',
                'inclusions': [
                    '2 Private Game Drives (Morning & Afternoon)',
                    'Luxury En-Suite Tented Safari Suite',
                    'Alfresco Candlelit Bush Dinner & Campfire BBQ',
                    'All Gourmet Meals, Wine & Jungle Cocktails',
                    'Complimentary Airport / Hotel Pickup & Dropoff'
                ],
                'highlights': 'Full immersion in Yala buffer wilderness, night stargazing, wildlife calls, luxury glamping.',
                'featured': True
            },
            {
                'id': 'yala-photo-safari',
                'category': 'photography',
                'category_label': 'PHOTOGRAPHY SPECIAL',
                'tag_class': 'tag-sage',
                'title': 'Wildlife Photographers Special Expedition',
                'subtitle': 'Customized jeep layout with specialized monopod mounts and extended hides.',
                'price': '$290',
                'price_unit': 'per custom 4x4 jeep (max 3 photographers)',
                'duration': 'Full Day / Flexible Timing',
                'vehicle': 'Custom Low-Angle Monopod Mount 4x4 Cruiser',
                'inclusions': [
                    'Pro Photographer Naturalist Tracker',
                    'Priority Early Entrance Park Permits',
                    'Dust Protection Camera Covers & Power Outlets',
                    'Gourmet Meals & All-Day Refreshments'
                ],
                'highlights': 'Dedicated positioning at leopard resting trees, golden hour waterhole hides.',
                'featured': False
            }
        ]
    }
    return render(request, 'core/packages.html', context)

