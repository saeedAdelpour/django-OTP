from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from .class_base_views import SnippetList, SnippetDetail, UserList, UserDetail, SnippetHighlight, SnippetViewSet, UserViewSet
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('snippets', SnippetViewSet)
router.register('users', UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]