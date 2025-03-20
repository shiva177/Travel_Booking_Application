from django.db import models
from django.contrib.auth.models import User
from travels.models import TravelOption
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    booking_id = models.CharField(max_length=10, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    num_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Confirmed')
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate a unique booking ID
            random_id = str(uuid.uuid4().int)[:8]
            self.booking_id = f"B{random_id}"
            
        # If this is a new booking and status is Confirmed, update available seats
        if not self.pk and self.status == 'Confirmed':
            self.travel_option.available_seats -= self.num_seats
            self.travel_option.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.user.username} ({self.travel_option})"
    
    class Meta:
        ordering = ['-booking_date']

