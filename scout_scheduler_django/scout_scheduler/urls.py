from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls')),    
    # redirect straight to bookings to see current.
    path('', RedirectView.as_view(pattern_name='booking:list', permanent=False)),
]