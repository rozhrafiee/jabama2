from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', include('reservation.urls')),
    path('users/', include('user.urls')),
    path('owners/', include('owner.urls')),
]
