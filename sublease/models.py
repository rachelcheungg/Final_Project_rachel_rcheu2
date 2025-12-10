from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Sublease(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subleases')
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_from = models.DateField(null=True, blank=True)
    available_to = models.DateField(null=True, blank=True)
    available_text = models.CharField(max_length=255, blank=True, help_text="Optional: e.g., 'June–August 2025' or 'Flexible'")
    description = models.TextField(blank=True)
    cover_photo = models.ImageField(upload_to='sublease_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.address} – ${self.price}"


class SubleasePhoto(models.Model):
    sublease = models.ForeignKey(Sublease, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='sublease_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.sublease.address}"