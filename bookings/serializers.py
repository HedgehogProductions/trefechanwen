from .models import Booking, Property
from rest_framework import serializers


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Booking
        fields = ('property', 'start_date', 'end_date')

class PropertySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Property
        fields = ('__all__')
