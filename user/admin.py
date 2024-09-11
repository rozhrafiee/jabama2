from django.contrib import admin
from .models import Renter

@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet', 'is_renter')
    search_fields = ('user__username',)
    list_filter = ('is_renter',)
