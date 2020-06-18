from datetime import timedelta, datetime, date
from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save

PUBLISH_CHOICES = [
  ('draft', 'Draft'),
  ('publish', 'Publish'),
  ('private', 'Private'),
]

from .validators import saeedValidate, signValidate

class Product(models.Model):
  title = models.CharField(max_length=15, unique=True, error_messages={'unique': 'not unique'}, help_text='your post title')
  slug = models.SlugField(null=True, blank=True)
  publish_on = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
  publish = models.CharField(max_length=15, choices=PUBLISH_CHOICES, default='draft')
  email = models.EmailField(max_length=200, null=True, blank=True)
  update_on = models.DateTimeField(auto_now=True)
  timestamp = models.DateTimeField(auto_now_add=True)

  # for naming in django admin
  class Meta:
    verbose_name = 'product'
    verbose_name_plural = 'product'
    # unique_together = [('title', 'slug')]

  def __str__(self):
    return smart_text(self.title)

  @property
  def age(self):
    now = datetime.now()
    publish_time = datetime.combine(self.publish_on, datetime.now().min.time())
    try:
      difference = now - publish_time
    except:
      return 'unknown'
    if difference <= timedelta(minutes=1):
      return 'just now'
    return "{} ago".format(timesince(publish_time).split(", ")[0])

  # not recommanded
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

def product_pre_save_reciever(sender, instance, *args, **kwargs):
  instance.update_on = timezone.now()
  if not instance.slug and instance.title:
    instance.slug = slugify(instance.title)

pre_save.connect(product_pre_save_reciever, sender=Product)

def product_post_save_reciever(sender, instance, created, *args, **kwargs):
  print('after save')

post_save.connect(product_post_save_reciever, sender=Product)