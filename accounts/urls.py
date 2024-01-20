from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
urlpatterns = [

    path('dashboard/', views.UserProfileView.as_view(), name='dashboard'),
     path('profile_update/', views.UserAccountUpdateView.as_view(), name='profile_update' ),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]