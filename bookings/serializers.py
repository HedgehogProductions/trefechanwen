from .models import AvailabilityDate, Booking, Property, PricingPeriod
from rest_framework import serializers


class AvailabilityDateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AvailabilityDate
        fields = ('date', 'cottage_booking_status', 'barn_booking_status')

class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = ('property', 'start_date', 'end_date')

class PropertySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Property
        fields = ('__all__')

class PricingPeriodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PricingPeriod
        fields = ('property', 'start_date', 'end_date', 'price')