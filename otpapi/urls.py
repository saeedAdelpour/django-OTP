from django.urls import path, include
from .views import enter, verify, create, change

urlpatterns = [
    path('enter/', enter, name='enter'),
    path('verify/', verify, name='verify'),
    path('create/', create, name='create'),
    path('change/', change, name='change'),
]
