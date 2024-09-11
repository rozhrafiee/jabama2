from django.urls import path
from .views import (
    welcome,
    place_list,
    place_detail,
    new_reservation,
    delete_reservation,
    PlaceView,
    PlaceDetails,
    PlaceCreateView,
    PlaceUpdate,
    PlaceDelete,
    ReservationView,
    ReservationCreateView,
    ReservationDelete
)

urlpatterns = [
    path('welcome/', welcome, name='welcome'),
    path('places/', place_list, name='place-list'),
    path('places/<int:id>/', place_detail, name='place-detail'),
    path('reservations/new/', new_reservation, name='new-reservation'),
    path('reservations/delete/<int:reservation_id>/', delete_reservation, name='delete-reservation'),
    
    path('api/places/', PlaceView.as_view(), name='api-place-list'),
    path('api/places/<int:pk>/', PlaceDetails.as_view(), name='api-place-detail'),
    path('api/places/create/', PlaceCreateView.as_view(), name='api-place-create'),
    path('api/places/update/<int:pk>/', PlaceUpdate.as_view(), name='api-place-update'),
    path('api/places/delete/<int:pk>/', PlaceDelete.as_view(), name='api-place-delete'),
    
    path('api/reservations/', ReservationView.as_view(), name='api-reservation-list'),
    path('api/reservations/create/', ReservationCreateView.as_view(), name='api-reservation-create'),
    path('api/reservations/delete/<int:pk>/', ReservationDelete.as_view(), name='api-reservation-delete'),
]
