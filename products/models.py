from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify

PUBLISH_CHOICES = [
  ('draft', 'Draft'),
  ('publish', 'Publish'),
  ('private', 'Private'),
]

from .validators import saeedValidate, signValidate

class Product(models.Model):
  title = models.CharField(max_length=15)
  slug = models.SlugField(null=True, blank=True)
  add_on = models.DateTimeField(auto_now=True)
  update_on = models.DateTimeField(default=timezone.now)
  publish = models.CharField(max_length=15, choices=PUBLISH_CHOICES, default='draft')
  email = models.EmailField(max_length=200, null=True, blank=True)

  # for naming in django admin
  class Meta:
    verbose_name = 'product'
    verbose_name_plural = 'product'
    # unique_together = [('title', 'slug')]

  def __str__(self):
    return smart_text(self.title)

  # not recommanded
  def save(self, *args, **kwargs):
    if not self.slug and self.title:
      self.slug = slugify(self.title)
    super().save(*args, **kwargs)