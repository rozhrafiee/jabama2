from django.db import models
from django.contrib.auth.models import User

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_renter = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username}"
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)