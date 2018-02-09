import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import AvailabilityDate, Booking, Property
from .serializers import AvailabilityDateSerializer, BookingSerializer, PropertySerializer

# Create your views here.
class AvailabilityDateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows availability dates to be viewed or edited.
    """

    serializer_class = AvailabilityDateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the dates
        between the start and end dates determined by the URL.
        """
        queryset = AvailabilityDate.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date is not None:
            queryset = queryset.filter(date__gte=start_date)
        if end_date is not None:
            queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('-date')

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """

    queryset = Booking.objects.all().order_by('-start_date')
    serializer_class = BookingSerializer

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """

    queryset = Property.objects.all().order_by('-name')
    serializer_class = PropertySerializer