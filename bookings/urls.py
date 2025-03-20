from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking-list'),
    path('<str:booking_id>/', views.booking_detail, name='booking-detail'),
    path('create/<str:travel_id>/', views.booking_create, name='booking-create'),
    path('<str:booking_id>/cancel/', views.booking_cancel, name='booking-cancel'),
]

