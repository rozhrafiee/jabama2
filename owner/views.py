from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Owner
from .serializers import OwnerSerializer, OwnerCreateSerializer
from user.permissions import IsSuperUser, IsOwner

class OwnerListView(ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsSuperUser]

class OwnerDetailView(RetrieveAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, IsOwner]  

class OwnerCreateView(CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        renter = self.request.user.renter 
        serializer.save(renter=renter)

class OwnerUpdateView(UpdateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class OwnerDeleteView(DestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated, IsOwner]
