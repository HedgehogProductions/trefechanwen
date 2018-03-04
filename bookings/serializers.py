from .models import AvailabilityDate, Booking, Property, PricingPeriod
from rest_framework import serializers


class AvailabilityDateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AvailabilityDate
        fields = ('date', 'cottage_booking_status', 'barn_booking_status', 'cottage_week_price', 'barn_week_price')
