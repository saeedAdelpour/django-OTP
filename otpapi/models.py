from django.db import models
from random import random

class Client(models.Model):
  name = models.CharField(max_length=10)
  number = models.IntegerField(unique=True)
  otp = models.IntegerField(null=True)
  logged_in = models.BooleanField(default=False)

  def set_otp(self):
    self.otp = int(random() * 10 ** 4)
  
  def set_none_otp(self):
    self.otp = None
  
  def login(self):
    self.logged_in = True

  def logout(self):
    self.logged_in = False

  def is_auth(self):
    return self.logged_in

  def __str__(self):
    return "-".join([item for item in ["client_object", self.name, str(self.number)] if item])

class Session(models.Model):
  client = models.ForeignKey(Client, on_delete=models.CASCADE)
  user_agent = models.CharField(max_length=50)