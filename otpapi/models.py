from django.db import models
from random import random

class Client(models.Model):
  name = models.CharField(max_length=10)
  number = models.IntegerField(unique=True)
  otp = models.IntegerField()

  def set_otp(self):
    self.otp = int(random() * 10 ** 4)
