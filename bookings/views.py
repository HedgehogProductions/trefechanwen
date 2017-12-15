from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Booking, Property
from .serializers import BookingSerializer, PropertySerializer

# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """

    queryset = Booking.objects.all().order_by('-start_date')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """

    queryset = Property.objects.all().order_by('-name')
    serializer_class = PropertySerializer