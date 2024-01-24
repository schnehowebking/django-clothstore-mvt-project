from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('category/<slug:category_slug>/', views.shop, name='products_by_category'),
    path('size/<slug:size_slug>/', views.shop, name='products_by_size'),
    path('color/<slug:color_slug>/', views.shop, name='products_by_color'),
    path('details/<int:product_id>/', views.ProductDetailsPageView.as_view(), name="productDetailspage"),
    path('details/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('buy/<int:product_id>/', views.BuyProductView.as_view(), name='buy_product'),
    path('cartbuy/', views.BuyCartProductView.as_view(), name='cartbuy_product'),
    path('wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
   
]