from django.db import models
from user.models import Renter  

class Owner(models.Model):
    renter = models.OneToOneField(Renter, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.renter.user.username}"  
