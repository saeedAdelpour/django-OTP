from django.urls import path
from .views import my_form

urlpatterns = [
  path('form/', my_form, name='form')
]