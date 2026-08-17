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

def blog(request):
    context = {
        'title': 'Yala Wildlife Blog & Field Journal | Yala Leopard Tracks',
        'featured_article': {
            'id': 'tracking-ghosts-yala-leopards',
            'category': 'Leopard Sightings',
            'category_code': 'leopard',
            'title': 'Tracking the Ghosts of Yala: A Senior Naturalist’s Guide to Spotting Leopards in Block 1',
            'author': 'Naturalist Kapila Ratnayake',
            'author_role': 'Senior Track Leader (18 Yrs Experience)',
            'date': 'August 14, 2026',
            'read_time': '6 min read',
            'excerpt': 'With the highest leopard density in the world, Yala Block 1 is the undisputed kingdom of Panthera pardus kotiya. Here is how our trackers decode alarm calls, territorial claw marks, and palu tree shadows.',
            'image': 'images/yala-leopard-card.jpg',
            'highlights': 'Palu tree canopy hides, territorial roar analysis, waterhole ambush tactics.'
        },
        'articles': [
            {
                'id': 'sloth-bear-palu-season',
                'category': 'Wildlife Behavior',
                'category_code': 'behavior',
                'tag_class': 'tag-amber',
                'title': 'Understanding Sri Lankan Sloth Bears: Seasonal Palu Fruit Feeding Habits',
                'author': 'Dr. Nimal Weerasinghe',
                'date': 'August 08, 2026',
                'read_time': '5 min read',
                'excerpt': 'During the summer fruiting season, Yala’s elusive sloth bears venture out onto low branches. Learn how to spot them safely.',
                'image': 'images/yala-wildlife-hero.jpg'
            },
            {
                'id': 'safari-photography-guide',
                'category': 'Photography Tips',
                'category_code': 'photography',
                'tag_class': 'tag-sage',
                'title': 'Best Lenses & Camera Settings for Dust-Free Safari Photography in Yala',
                'author': 'Sahan Wickramasinghe',
                'date': 'July 29, 2026',
                'read_time': '7 min read',
                'excerpt': 'Navigating dust clouds, harsh tropical sunlight, and sudden speed movements requires specific shutter speeds and monopod positioning.',
                'image': 'images/jeep-safari.jpg'
            },
            {
                'id': 'elephant-corridors-gathering',
                'category': 'Conservation',
                'category_code': 'conservation',
                'tag_class': 'tag-rose',
                'title': 'The Great Elephant Gathering: Udawalawe & Minneriya Migration Corridors',
                'author': 'Conservation Team',
                'date': 'July 18, 2026',
                'read_time': '8 min read',
                'excerpt': 'How ancient elephant migration pathways connect Yala, Lunugamvehera, and Udawalawe national parks into one sanctuary corridor.',
                'image': 'images/campsite-yala.jpg'
            },
            {
                'id': 'manik-river-bush-dining',
                'category': 'Jungle Culture',
                'category_code': 'culture',
                'tag_class': 'tag-terracotta',
                'title': 'Why Manik River Bush Dining is Yala’s Most Iconic Wilderness Culinary Experience',
                'author': 'Chef Dammika Perera',
                'date': 'July 05, 2026',
                'read_time': '4 min read',
                'excerpt': 'Dining under the canopy of ancient Kumbuk trees along the Manik River. Fresh clay-pot curries and starlit lantern barbecues.',
                'image': 'images/jungle-cuisine.jpg'
            },
            {
                'id': 'ethical-wildlife-tracking-rules',
                'category': 'Conservation',
                'category_code': 'conservation',
                'tag_class': 'tag-sage',
                'title': 'Ethical Wildlife Observation Rules: Protecting Yala Block 1 Habitat',
                'author': 'Yala Leopard Tracks Team',
                'date': 'June 22, 2026',
                'read_time': '5 min read',
                'excerpt': 'Our Nature First policy strictly enforces off-road boundaries, engine noise reduction, and safe distance guidelines for ethical viewing.',
                'image': 'images/hero-safari-jeep.jpg'
            }
        ]
    }
    return render(request, 'core/blog.html', context)

def tours(request):
    context = {
        'title': 'Sri Lanka Tours & Islandwide Private Transport | Yala Leopard Tracks',
        'tours_list': [
            {
                'id': 'grand-wildlife-circuit',
                'category': 'round-tour',
                'category_label': '7-DAY ROUND TOUR',
                'tag_class': 'tag-sage',
                'title': '7-Day Sri Lanka Grand Wildlife & Heritage Circuit',
                'subtitle': 'The ultimate islandwide expedition covering Yala leopards, Wilpattu sloth bears, Sigiriya Rock, and Mirissa blue whales.',
                'price': '$580',
                'price_unit': 'per private A/C van (up to 4 guests)',
                'duration': '7 Days / 6 Nights',
                'vehicle': 'Private Luxury Toyota KDH Air-Conditioned Van',
                'inclusions': [
                    'English-Speaking Professional Driver-Guide',
                    'All Fuel, Toll Fees, & Parking Charges',
                    'Driver Accommodation & Meals Included',
                    'Chilled Bottled Mineral Water Daily',
                    'Door-to-Door Airport Pickup & Dropoff'
                ],
                'route': 'Colombo → Wilpattu → Sigiriya → Kandy → Udawalawe → Yala → Mirissa → Airport',
                'featured': True
            },
            {
                'id': 'southern-parks-coastal',
                'category': 'round-tour',
                'category_label': '4-DAY TOUR',
                'tag_class': 'tag-amber',
                'title': '4-Day Southern Wildlife & Coastal Fort Tour',
                'subtitle': 'Experience wild elephants at Udawalawe, Yala leopard game drives, and UNESCO Galle Dutch Fort.',
                'price': '$320',
                'price_unit': 'per private A/C sedan or mini van',
                'duration': '4 Days / 3 Nights',
                'vehicle': 'Private A/C Toyota Prius / Axio Sedan',
                'inclusions': [
                    'Dedicated Chauffeur Driver',
                    'Highway Express Tolls & Fuel',
                    'Cold Towels & Bottled Refreshments',
                    'Flexible Stops for Photo Spots & Tea Shops'
                ],
                'route': 'Colombo / Airport → Udawalawe → Yala National Park → Galle Fort → Colombo',
                'featured': True
            },
            {
                'id': 'yala-ella-transfer',
                'category': 'transfer',
                'category_label': 'INTERCITY SHUTTLE',
                'tag_class': 'tag-terracotta',
                'title': 'Yala / Tissa to Ella Scenic Mountain Transfer',
                'subtitle': 'Comfortable private shuttle connecting Yala jungle camps with Ella tea country.',
                'price': '$65',
                'price_unit': 'per private vehicle (up to 3 guests)',
                'duration': '2.5 Hours Direct',
                'vehicle': 'Private A/C Sedan or SUV',
                'inclusions': [
                    'Door-to-Door Hotel Pickup & Dropoff',
                    'Photo Stop at Ravana Waterfalls',
                    'Luggage Handling & Bottled Water'
                ],
                'route': 'Yala Campsite / Tissamaharama → Ella Town / Nine Arches Bridge',
                'featured': False
            },
            {
                'id': 'cmb-airport-transfer',
                'category': 'transfer',
                'category_label': 'AIRPORT SHUTTLE (24/7)',
                'tag_class': 'tag-rose',
                'title': 'CMB Airport Express Transfer to Yala & Tissamaharama',
                'subtitle': '24/7 direct Southern Expressway airport transfer with flight arrival tracking.',
                'price': '$85',
                'price_unit': 'per private A/C vehicle',
                'duration': '3.5 Hours Express Highway',
                'vehicle': 'Comfortable Private A/C Sedan / Van',
                'inclusions': [
                    'Meet & Greet at CMB Arrival Gate with Name Board',
                    'Southern Expressway Toll Fees Included',
                    'Flight Delay Tracking (No Extra Charge)',
                    'Chilled Mineral Water & Reclining Seats'
                ],
                'route': 'Bandaranaike International Airport (CMB) ↔ Yala Gate / Hotel',
                'featured': True
            },
            {
                'id': 'cultural-triangle-express',
                'category': 'round-tour',
                'category_label': '3-DAY TOUR',
                'tag_class': 'tag-sage',
                'title': '3-Day Cultural Triangle & Minneriya Elephant Gathering',
                'subtitle': 'Climb Sigiriya Lion Rock Fortress, explore Dambulla Cave Temple, and track elephant herds.',
                'price': '$270',
                'price_unit': 'per private vehicle',
                'duration': '3 Days / 2 Nights',
                'vehicle': 'Private A/C Sedan / SUV',
                'inclusions': [
                    'Experienced Chauffeur Guide',
                    'All Transport Fuel & Toll Fees',
                    'Hotel Pickup & Dropoff'
                ],
                'route': 'Colombo → Dambulla → Sigiriya Rock → Minneriya Safari → Yala',
                'featured': False
            },
            {
                'id': 'chauffeur-daily-hire',
                'category': 'fleet',
                'category_label': 'DAILY CHAUFFEUR HIRE',
                'tag_class': 'tag-amber',
                'title': 'Private Chauffeur-Driven Daily Vehicle Hire',
                'subtitle': 'Hire a dedicated private vehicle with driver per day for customized Sri Lanka exploring.',
                'price': '$60',
                'price_unit': 'per day (100 km included daily)',
                'duration': 'Per Day / Flexible Days',
                'vehicle': 'Sedan, Luxury Van, or 4x4 Cruiser Choice',
                'inclusions': [
                    'Dedicated Driver & Chauffeur Allowance',
                    'Fuel, Insurance, & Maintenance Included',
                    '100 km Daily Mileage Allowance',
                    'Flexible Custom Daily Itinerary'
                ],
                'route': 'Custom Itinerary Anywhere Across Sri Lanka',
                'featured': False
            }
        ]
    }
    return render(request, 'core/tours.html', context)



