from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet

rounder = DefaultRouter()
rounder.register(r'notifications', NotificationViewSet, basename='notification')
urlpatterns = [
    path('notifications', include(rounder.urls)),
]