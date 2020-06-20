from django.db import models
from random import random

class Client(models.Model):
  name = models.CharField(max_length=10)
  number = models.IntegerField(unique=True)
  otp = models.IntegerField(null=True)

  def set_otp(self):
    self.otp = int(random() * 10 ** 4)
  
  def set_none_otp(self):
    self.otp = None

  def __str__(self):
    return "-".join([item for item in ["client_object", self.name, str(self.number)] if item])

class Session(models.Model):
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  user_agent = models.CharField(max_length=50)