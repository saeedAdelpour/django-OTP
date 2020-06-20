from django.contrib import admin
from .models import Client, Session

class ClientManager(admin.ModelAdmin):
  list_display = ["name", "number", "otp", "logged_in"]

class SessionManager(admin.ModelAdmin):
  list_display = ["client", "user_agent"]

admin.site.register(Session, SessionManager)
admin.site.register(Client, ClientManager)