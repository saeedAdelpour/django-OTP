from django.shortcuts import render
from .serializer import DrinkSerializer
class DrinkViewSet(viewsets.ModelViewSet):
  queryset = Drink.objects.all()
  serializer_class = DrinkSerializer

# Create your views here.
