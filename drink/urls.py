from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DrinkViewSet, UserViewSet

router = DefaultRouter()
router.register('drink', DrinkViewSet)
router.register('user', UserViewSet)


urlpatterns = [
  path('', include(router.urls)),
]