from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'bookings'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('travels/', views.travel_list, name='travel_list'),
    path('travels/<int:travel_id>/', views.travel_detail, name='travel_detail'),
    path('travels/<int:travel_id>/book/', views.book_travel, name='book_travel'),
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Admin Panel
    path('admin/', admin.site.urls),

    # Include 'bookings' app URLs (correct way)
    path('bookings/', include('apps.bookings.urls')),

]
