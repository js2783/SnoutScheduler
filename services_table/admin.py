from django.contrib import admin
from .models import Post, Service  

# Keep your teammate’s Post model
admin.site.register(Post)

# Register the Service model so it appears in the admin panel
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "duration_minutes", "formatted_price", "active")
    list_filter = ("active", "category")
    search_fields = ("name", "description")
