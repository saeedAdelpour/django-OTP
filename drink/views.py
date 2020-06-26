from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from .models import Drink
from .serializer import DrinkSerializer, UserSerializer
class DrinkViewSet(viewsets.ModelViewSet):
  queryset = Drink.objects.all()
  serializer_class = DrinkSerializer

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
