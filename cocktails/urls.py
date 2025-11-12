from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.get_queryset, name='index'),
    path('cocktail/<int:pk>/', views.show_cocktail, name='cocktail'),
    path('order/<int:cocktail_id>/', views.order, name='order'),
    path('taste/<int:taste_id>/', views.show_category, name='cocks'),
    path('rules/', views.show_rules, name='rules'),
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('alcohol/<int:alcohol_id>/', views.show_alcohol, name='cocks'),
    path('refresh/', views.refresh_cock, name='refresh'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)