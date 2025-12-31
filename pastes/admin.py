from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Paste

@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "expires_at", "max_views", "views")
