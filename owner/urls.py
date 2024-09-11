from django.urls import path
from .views import OwnerDetailView

urlpatterns = [
    path('owners/<int:pk>/', OwnerDetailView.as_view(), name='owner-detail'),
]
