from django.urls import path
from . import views
from .views import NewsListView, NewsDetailView, subscribe

from .views import gallery_image_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('classes/', views.classes, name='classes'),
    path('nursery/', views.nursery, name='nursery'),
    path('primary/', views.primary, name='primary'),
    path('campus/', views.campus, name='campus'),
    path('main/', views.main, name='main'),
    path('annex/', views.annex, name='annex'),
    path('muni/', views.muni, name='muni'),
    path('golden/', views.golden, name='golden'),
    path('admissions/', views.admissions, name='admissions'),
  
    path('gallery/', views.gallery, name='gallery'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('subscribe/', subscribe, name='subscribe'),
     path('gallery/<int:pk>/', gallery_image_detail, name='gallery_detail'),
     
]
