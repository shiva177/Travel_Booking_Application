from django.db import models
import uuid

class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('Flight', 'Flight'),
        ('Train', 'Train'),
        ('Bus', 'Bus'),
    ]
    
    travel_id = models.CharField(max_length=10, unique=True, editable=False)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.travel_id:
            # Generate a unique travel ID based on type and random string
            prefix = self.type[0]  # F for Flight, T for Train, B for Bus
            random_id = str(uuid.uuid4().int)[:6]
            self.travel_id = f"{prefix}{random_id}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.travel_id} - {self.source} to {self.destination} ({self.type})"
    
    class Meta:
        ordering = ['departure_date', 'departure_time']

