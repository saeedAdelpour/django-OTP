from django.db import models

class Account(models.Model):
  name = models.CharField(max_length=10)
  phone_number = models.IntegerField(unique=True)
  otp_number = models.IntegerField(unique=True)

  def __str__(self):
    return " - ".join([self.name, str(self.phone_number)])