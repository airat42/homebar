from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('cocktail/<int:cocktail_id>/', views.show_cocktail, name='cocktail'),
    path('taste/<int:taste_id>/', views.show_category, name='cocks'),
    path('rules/', views.show_rules, name='rules'),
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('alcohol/<int:alcohol_id>/', views.show_alcohol, name='cocks'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)