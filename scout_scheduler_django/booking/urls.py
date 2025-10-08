from django.urls import path
from . import views
urlpatterns = [path('', views.book, name='book'), path('success/<str:ref>/', views.success, name='success')]
