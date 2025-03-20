from django.contrib import admin #gives access to Django’s built-in admin tools
from .models import TravelOption

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'type', 'source', 'destination', 'departure_date', 'departure_time', 'price', 'available_seats')
    list_filter = ('type', 'source', 'destination', 'departure_date')
    search_fields = ('travel_id', 'source', 'destination')
    date_hierarchy = 'departure_date'

