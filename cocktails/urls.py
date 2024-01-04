from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.get_queryset, name='index'),
    path('cocktail/<int:cocktail_id>/', views.show_cocktail, name='cocktail'),
    path('taste/<int:taste_id>/', views.show_category, name='cocks'),
    path('rules/', views.show_rules, name='rules'),
    path('base/', views.show_bills, name='base'),
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('alcohol/<int:alcohol_id>/', views.show_alcohol, name='cocks'),
    path('order/<int:cocktail_id>/', views.order, name='order'),
    path('refresh/', views.refresh_cock, name='refresh')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)