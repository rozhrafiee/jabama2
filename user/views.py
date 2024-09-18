# user/views.py
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Renter, Wallet
from .serializers import RenterSerializer, RenterCreateSerializer, WalletUpdateSerializer
from django.contrib.auth.models import User
from user.permissions import IsRenter, IsSuperUser

class RenterListView(ListAPIView):
    queryset = Renter.objects.all()
    serializer_class = RenterSerializer
    permission_classes = [IsSuperUser] 

class RenterDetailView(RetrieveAPIView):
    queryset = Renter.objects.all()
    serializer_class = RenterSerializer
    permission_classes = [IsAuthenticated, IsRenter]  

class RenterCreateView(CreateAPIView):
    queryset = Renter.objects.all()
    serializer_class = RenterCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user  
        serializer.save(user=user)

class WalletUpdateView(UpdateAPIView):
    queryset = Renter.objects.all()
    serializer_class = WalletUpdateSerializer
    permission_classes = [IsAuthenticated, IsRenter]

    def get_object(self):
        return self.request.user.renter 


