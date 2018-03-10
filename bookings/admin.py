from django.contrib import admin

from .models import Booking, Property, AvailabilityDate, PricingPeriod

from .booking_form import BookingForm
from .pricing_period_form import PricingPeriodForm


class BookingAdmin(admin.ModelAdmin):
    view_on_site = False
    exclude = ('dates',)
    form = BookingForm
    list_display = ('property', 'start_date', 'end_date', 'customer_name')
    list_filter = ('property', 'start_date',)

class AvailabilityAdmin(admin.ModelAdmin):
    view_on_site = False
    list_display = ('date', 'cottage_booking_status', 'barn_booking_status',
                    'cottage_week_price', 'cottage_week_price_discount', 'barn_week_price', 'barn_week_price_discount')
    list_filter = ('date', 'cottage_booking_status', 'barn_booking_status',)

class PropertyAdmin(admin.ModelAdmin):
    view_on_site = False

class PricingPeriodAdmin(admin.ModelAdmin):
    view_on_site = False
    exclude = ('dates',)
    form = PricingPeriodForm
    list_display = ('property', 'start_date', 'end_date', 'price', 'discount')
    list_filter = ('property', 'start_date',)


# Register your models here.
admin.site.register(AvailabilityDate, AvailabilityAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PricingPeriod, PricingPeriodAdmin)
