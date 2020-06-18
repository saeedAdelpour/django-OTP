from django.db import models

PUBLISH_CHOICES = [
  ('draft', 'Draft'),
  ('publish', 'Publish'),
  ('private', 'Private'),
]

class Product(models.Model):
  title = models.CharField(max_length=15)
  add_on = models.DateTimeField()
  publish = models.CharField(max_length=15, choices=PUBLISH_CHOICES, default='draft')

  # for naming in django admin
  class Meta:
    verbose_name = 'product'
    verbose_name_plural = 'product'