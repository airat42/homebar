from django.urls import path

import cocktails.views_auth
import cocktails.views_ordering
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.get_index, name='index'),
    path('cocktail/<int:pk>/', views.show_cocktail, name='cocktail'),
    path('just_drink/', cocktails.views_ordering.just_drink, name='just_drink'),
    path('order/<int:cocktail_id>/', cocktails.views_ordering.order, name='order'),
    path('order_drink/', cocktails.views_ordering.order_drink, name='order_drink'),
    path('rules/', views.show_rules, name='rules'),
    path('qr/', views.get_qr, name='qr'),
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('refresh/', views.refresh_cock, name='refresh'),
    path('register/', cocktails.views_auth.register_view, name='register'),
    path('login/', cocktails.views_auth.login_view, name='login'),
    path('logout/', cocktails.views_auth.logout_view, name='logout'),
    path('bill/<int:bill_id>/completed/', cocktails.views_ordering.mark_completed, name='mark_completed'),
    path('bill/<int:bill_id>/canceled/', cocktails.views_ordering.mark_canceled, name='mark_canceled'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)