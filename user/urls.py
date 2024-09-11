from django.urls import path
from .views import RenterDetailView

urlpatterns = [
    path('renters/<int:pk>/', RenterDetailView.as_view(), name='renter-detail'),
]
