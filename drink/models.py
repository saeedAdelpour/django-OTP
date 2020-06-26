from django.db import models
from django.contrib.auth.models import User

addition_choices = [(item, item) for item in ["mocha", "soy"]]

class Drink(models.Model):
  name = models.CharField(max_length=15)
  addition = models.CharField(max_length=15, choices=addition_choices)
  created = models.DateField(auto_now_add=True)
  owner = models.ForeignKey(User, related_name='drinks',on_delete=models.CASCADE)