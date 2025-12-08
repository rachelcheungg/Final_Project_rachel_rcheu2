from django.db import models

class Apartment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    rent_amount = models.DecimalField(decimal_places=2, max_digits=10)
    is_available = models.BooleanField(default=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    longitude = models.DecimalField(decimal_places=6, max_digits=9)

    def __str__(self):
        return f"{self.name}"
