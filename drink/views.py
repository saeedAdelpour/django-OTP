from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Drink
from .serializer import DrinkSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

class DrinkViewSet(viewsets.ModelViewSet):
  queryset = Drink.objects.all()
  serializer_class = DrinkSerializer
  permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]
