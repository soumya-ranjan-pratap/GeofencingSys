from django.db import models

class CheckInOut(models.Model):
    username = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)     # Latitude of the user's location
    longitude = models.FloatField(null=True, blank=True)    # Longitude of the user's location
    check_in = models.DateTimeField(null=True, blank=True)  # Allows null values for Check-In timestamp
    check_out = models.DateTimeField(null=True, blank=True) # Allows null values for Check-Out timestamp

    def __str__(self):
        return f"{self.username} - Check-in: {self.check_in}, Check-out: {self.check_out}"
