from django.db import models

# Create your models here.

class CheckInOut(models.Model):
    username = models.CharField(max_length=100)
    check_in = models.DateTimeField(null=True, blank=True)   # Allows null values
    check_out = models.DateTimeField(null=True, blank=True)  # Allows null values

    def __str__(self):
        return f"{self.username} - Check-in: {self.check_in}, Check-out: {self.check_out}"
