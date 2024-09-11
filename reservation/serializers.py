from rest_framework import serializers
from .models import Place, Reservation

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()  # Nested serializer for Place
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Assuming you're using a ForeignKey or similar field for user

    class Meta:
        model = Reservation
        fields = '__all__'
