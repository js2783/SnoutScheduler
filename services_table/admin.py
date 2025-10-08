from django.contrib import admin

from django.contrib import admin
from .models import Post

admin.site.register(Post)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "duration_minutes", "formatted_price", "active")
    list_filter = ("active", "category")
    search_fields = ("name", "description")

