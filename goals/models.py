from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FinancialTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField(blank=True, null=True)

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def is_completed(self):
        return self.current_amount >= self.target_amount

    def __str__(self):
        return self.name