from django.contrib import admin
from .models import Place, Reservation

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_night', 'max_guests')
    search_fields = ('name', 'location')
    list_filter = ('location',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'check_in_time', 'check_out_time', 'guests', 'created_at')
    search_fields = ('user__username', 'place__name')
    list_filter = ('check_in_time', 'check_out_time')
