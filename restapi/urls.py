from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .class_base_views import SnippetList, SnippetDetail
from . import views

urlpatterns = [
    path('snippets/', SnippetList.as_view()),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)