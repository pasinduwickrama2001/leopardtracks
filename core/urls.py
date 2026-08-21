from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('book/', views.create_booking, name='create_booking'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('tours/', views.tours, name='tours'),
    path('tours/<slug:slug>/', views.tour_detail, name='tour_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('tickets/', views.tickets, name='tickets'),
    path('policies/', views.policies, name='policies'),
]

