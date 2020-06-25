from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .class_base_views import SnippetList, SnippetDetail, UserList, UserDetail, SnippetHighlight
from . import views

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('', views.api_root),
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', SnippetHighlight.as_view(), name='snippet-highlight'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]

urlpatterns += format_suffix_patterns([
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])