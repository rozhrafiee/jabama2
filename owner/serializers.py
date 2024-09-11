from rest_framework import serializers
from .models import Owner
from user.models import Renter  

class OwnerSerializer(serializers.ModelSerializer):
    renter = serializers.StringRelatedField()  

    class Meta:
        model = Owner
        fields = ['id', 'renter']


class OwnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['renter']

    def validate_renter(self, value):
        if Owner.objects.filter(renter=value).exists():
            raise serializers.ValidationError("This renter is already an owner.")
        return value
