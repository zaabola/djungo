from rest_framework.routers import DefaultRouter
from .views import SessionApiViewSet
from django.urls import path, include
router = DefaultRouter()
router.register('sessions', SessionApiViewSet, basename='session')
urlpatterns = [
    path('', include(router.urls)),
]