from django.contrib import admin
from .models import Client

class ClientManager(admin.ModelAdmin):
  list_display = ["name", "number", "otp"]

admin.site.register(Client, ClientManager)