from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages, name='packages'),
    path('blog/', views.blog, name='blog'),
    path('tours/', views.tours, name='tours'),
]
