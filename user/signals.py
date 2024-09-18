from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Renter, Wallet

@receiver(post_save, sender=Renter)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance.user)
        print(f"Wallet created for Renter {instance.user.username}")

@receiver(post_save, sender=Wallet)
def update_wallet(sender, instance, **kwargs):
    print(f"Wallet updated for {instance.user.username}, New amount: {instance.amount}")


