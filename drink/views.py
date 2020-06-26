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

  def get_queryset(self):
    request_name_filter = self.request.query_params.get("name")
    request_addition_filter = self.request.query_params.get("addition")

    if request_name_filter and request_addition_filter:
      queryset = Drink.objects.filter(name__icontains=request_name_filter, addition=request_name_filter)
    elif request_name_filter:
      queryset = Drink.objects.filter(name__icontains=request_name_filter)
    elif request_addition_filter:
      queryset = Drink.objects.filter(addition=request_name_filter)
    else:
      queryset = Drink.objects.all()

    return queryset

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]
