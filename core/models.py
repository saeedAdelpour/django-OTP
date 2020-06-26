from django.db import models

class Post(models.Model):
  title = models.CharField(max_length=20)
  description = models.TextField(max_length=200, null=True)
  created_on = models.DateField(auto_now_add=True)