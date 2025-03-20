from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'num_seats', 'total_price', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('booking_id', 'user__username', 'travel_option__travel_id')
    date_hierarchy = 'booking_date'

