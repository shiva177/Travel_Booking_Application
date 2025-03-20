from django.urls import path
from . import views

urlpatterns = [
    path('', views.travel_list, name='travel-list'),
    path('create/', views.travel_create, name='travel-create'),
    path('<str:travel_id>/update/', views.travel_update, name='travel-update'),
    path('<str:travel_id>/delete/', views.travel_delete, name='travel-delete'),
    path('<str:travel_id>/', views.travel_detail, name='travel-detail'),  # Generic path last
]

