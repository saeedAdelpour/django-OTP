from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Drink

class DrinkSerializer(serializers.ModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Drink
    fields = ["id", "name", "addition", "owner", "url"]

class UserSerializer(serializers.ModelSerializer):
  drinks = serializers.HyperlinkedRelatedField(many=True, view_name="drink-detail", read_only=True)

  class Meta:
    model = User
    fields = ["id", "username", "url", "drinks"]