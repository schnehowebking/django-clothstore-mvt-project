from django.urls import path, include
from . import views

urlpatterns = [
    path('contact/', views.contact , name='contact'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('', views.home , name='home'),
    path('<slug:category_slug>/', views.home, name='home'),
   
]