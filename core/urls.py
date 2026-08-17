from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('blog/', views.blog, name='blog'),
    path('tours/', views.tours, name='tours'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('reviews/', views.reviews, name='reviews'),
    path('tickets/', views.tickets, name='tickets'),
]
