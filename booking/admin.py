from django.contrib import admin
from .models import Customer, Booking

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','created_at')
    search_fields = ('first_name','last_name','phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','customer','appointment_date','appointment_time','api_ref','created_at')
    search_fields = ('customer__first_name','customer__last_name','api_ref')
    readonly_fields = ('created_at','updated_at')