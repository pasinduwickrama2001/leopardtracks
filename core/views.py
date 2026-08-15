from django.shortcuts import render

def home(request):
    context = {
        'title': 'Yala Trails | Safari & Wildlife Adventures',
        'featured_trails': [
            {'name': 'Yala Block 1 Safari', 'duration': '3 Hours', 'tag': 'Popular'},
            {'name': 'Kumana Bird Sanctuary Trail', 'duration': '4 Hours', 'tag': 'Scenic'},
            {'name': 'Lunugamvehera Wildlife Corridor', 'duration': '5 Hours', 'tag': 'Adventure'},
        ]
    }
    return render(request, 'core/home.html', context)
