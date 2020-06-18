from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
  fields = [
    'title',
    'slug',
    'publish_on',
    'publish',
    'email',
    'update_on',
    'timestamp',
    'overall_content',
    'age',
  ]
  readonly_fields = ['update_on', 'timestamp', 'overall_content', 'age']
  list_display = ['title', 'publish_on']

  def overall_content(self, instance, *args,  **kwargs):
    return " / ".join([
      str(item)
      for item in
      [instance.title, instance.publish_on, instance.publish, instance.email]
      if item
      ])

  # always recommanded
  class Meta:
    model = Product

admin.site.register(Product, ProductAdmin)