from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('new/', views.book, name='book'),
    path('success/<str:ref>/', views.success, name='success'),
    path('', views.bookings_list, name='list'),            
    path('<int:pk>/', views.booking_detail, name='detail'),
    path('availability/', views.availability_json, name='availability')
]