from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TravelOption(models.Model):
    TRAVEL_TYPES = (
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    )
    
    travel_id = models.AutoField(primary_key=True)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.get_travel_type_display()} from {self.source} to {self.destination} on {self.departure_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    num_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    
    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username} - {self.status}"
    
    def cancel(self):
        if self.status == 'confirmed':
            self.status = 'cancelled'
            self.travel_option.available_seats += self.num_seats
            self.travel_option.save()
            self.save()
            return True
        return False
