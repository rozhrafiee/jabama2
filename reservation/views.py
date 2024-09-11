from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from .serializers import PlaceSerializer, ReservationSerializer
from .models import Place, Reservation
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView,
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from user.permissions import IsOwner, IsSuperUser
from django.views.decorators.csrf import csrf_exempt
import json


# ----- Function-Based Views -----
def welcome(request):
    return render(request, "reservations/welcome.html")


def place_list(request):
    places = Place.objects.all()
    place_list = [{
        "ID": place.id,
        "name": place.name,
        "description": place.description,
        "location": place.location,
        "price_per_night": place.price_per_night,
        "max_guests": place.max_guests,
    } for place in places]

    return JsonResponse(place_list, safe=False)


def place_detail(request, id):
    try:
        place = Place.objects.get(id=id)
        place_dict = {
            "ID": place.id,
            "name": place.name,
            "description": place.description,
            "location": place.location,
            "price_per_night": place.price_per_night,
            "max_guests": place.max_guests,
        }
        return JsonResponse(place_dict)
    except Place.DoesNotExist:
        return HttpResponse("Place Not Found", status=404)


@csrf_exempt
def new_reservation(request):
    if request.method == "POST":
        body = json.loads(request.body)
        place = Place.objects.get(id=body["place_id"])
        if place.max_guests == 0:
            return HttpResponse("No Capacity")
        
        with transaction.atomic():
            reservation = Reservation.objects.create(
                place=place,
                user_id=body["user_id"],
                check_in_time=body["check_in"],
                check_out_time=body["check_out"],
                guests=body["guests"]
            )
            place.max_guests -= reservation.guests
            place.save()
        
        return HttpResponse(f"New reservation created for {reservation.user} at {place.name}")
    else:
        return HttpResponse("Bad Request", status=400)


@csrf_exempt
def delete_reservation(request, reservation_id):
    if request.method == "DELETE":
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            place = reservation.place
            place.max_guests += reservation.guests
            place.save()
            reservation.delete()
            return HttpResponse("Reservation Deleted")
        except Reservation.DoesNotExist:
            return HttpResponse("Reservation Not Found", status=404)
    else:
        return HttpResponse("Bad Request", status=400)

# ----- Class-Based Views -----

# Place Views
class PlaceView(ListAPIView):
    permission_classes = [IsSuperUser]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["price_per_night"]
    search_fields = ["name", "location"]
    filterset_fields = ['max_guests']


class PlaceDetails(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceCreateView(CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        owner = self.request.user.owner
        serializer.save(owner=owner)


class PlaceUpdate(UpdateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PlaceDelete(DestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated, IsOwner]


# Reservation Views
class ReservationView(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at"]
    search_fields = ["user__username", "place__name"]
    filterset_fields = ['place', 'guests']


class ReservationCreateView(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        place = serializer.validated_data['place']
        check_in_time = serializer.validated_data['check_in_time']
        check_out_time = serializer.validated_data['check_out_time']
        if check_out_time <= check_in_time:
            raise ValidationError("Check-out time must be after check-in time.")
        num_days = (check_out_time - check_in_time).days
        total_cost = num_days * place.price_per_night
        if user.wallet < total_cost:
            raise ValidationError("You don't have enough money to make this reservation.")
        with transaction.atomic():
            user.wallet -= total_cost
            place.owner.wallet += total_cost
            place.max_guests -= serializer.validated_data['guests']
            place.save()

            serializer.save(user=user, place=place)


class ReservationDelete(DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

