from rest_framework import serializers
from .models import Renter
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RenterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested User data for read operations

    class Meta:
        model = Renter
        fields = ['user', 'wallet', 'is_renter']

class RenterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = ['user', 'wallet']

class WalletUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = ['wallet']
