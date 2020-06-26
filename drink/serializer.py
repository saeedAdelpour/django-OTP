from rest_framework import serializers
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Drink
    fields = ["id", "name", "addition", "owner", "url"]
