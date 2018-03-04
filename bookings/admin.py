from django.contrib import admin
from django import forms
from datetime import timedelta, date
import logging

from django.db.models.signals import pre_delete

from django.dispatch import receiver

from .models import Booking, Property, AvailabilityDate, PricingPeriod

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


class PricingPeriodForm(forms.ModelForm):
    class Meta:
        model = PricingPeriod
        fields = '__all__'

    def clean(self):
        # Save original dates and property in case of change
        self.original_start_date = self.instance.start_date
        self.original_end_date = self.instance.end_date
        try:
            self.original_property = self.instance.property.name
        except:
            self.original_property = None

        # Check start date is not after end date
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date")

        return self.cleaned_data

    def save(self, commit=True):
        # do custom stuff
        logger = logging.getLogger(__name__)

        # save the basics so we have a database record to link to dates even if this is a new booking
        pricing_period = super(PricingPeriodForm, self).save(commit=False)
        pricing_period.save()

        # if the dates or property has changed:
        if self.changed_data:
            logger.error("Changing dates from: " + str(self.original_start_date) + " - " + str(self.original_end_date) +
            " to: " + str(self.cleaned_data.get('start_date')) + " - " + str(self.cleaned_data.get('end_date')) +
            "and property from: " + str(self.original_property) + " to: " + str(self.cleaned_data.get('property')))
        else:
            logger.error("No change")

        return pricing_period


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def clean(self):
        logger = logging.getLogger(__name__)
        # Save original dates and property in case of change
        self.original_start_date = self.instance.start_date
        self.original_end_date = self.instance.end_date
        try:
            self.original_property = self.instance.property.name
        except:
            self.original_property = None

        # Check start date is not after end date
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date > end_date:
            raise forms.ValidationError("Start date cannot be after end date")

        return self.cleaned_data

    def save(self, commit=True):
        # do custom stuff
        logger = logging.getLogger(__name__)

        # save the basics so we have a database record to link to dates even if this is a new booking
        booking = super(BookingForm, self).save(commit=False)
        booking.save()


        # if the dates or property has changed:
        logger.error("Changed: " + str(self.changed_data))
        if self.changed_data:
            logger.error("Changing dates from: " + str(self.original_start_date) + " - " + str(self.original_end_date) +
            " to: " + str(self.cleaned_data.get('start_date')) + " - " + str(self.cleaned_data.get('end_date')) +
            "and property from: " + str(self.original_property) + " to: " + str(self.cleaned_data.get('property')))

            # clear the property from the old dates - if there are any
            if self.original_start_date != None and self.original_end_date != None and self.original_property != None :
                logger.error("removing old dates from " + str(self.original_property))
                # Revert booking status on all 'AvailabilityDate's
                for oldBookingDate in daterange(self.original_start_date, self.original_end_date):
                    availabilityDate = AvailabilityDate.objects.get(date=oldBookingDate)

                    # Old Start date: (Changeover -> Booked AM) OR (Booked PM -> Free) else error
                    if oldBookingDate == self.original_start_date:
                        if str(self.original_property) == "Cottage":
                            logger.error("Cottage booking status changing from " + str(availabilityDate.cottage_booking_status))
                            if str(availabilityDate.cottage_booking_status) == "CH":
                                availabilityDate.cottage_booking_status = "AM"
                            elif str(availabilityDate.cottage_booking_status) == "PM":
                                availabilityDate.cottage_booking_status = "FR"
                            else:
                                logger.error("Status for Cottage should have been changeover or booked PM: " + str(availabilityDate))
                                raise ValueError("Booking status incorrect")
                        elif str(self.original_property) == "Barn":
                            if str(availabilityDate.barn_booking_status) == "CH":
                                availabilityDate.barn_booking_status = "AM"
                            elif str(availabilityDate.barn_booking_status) == "PM":
                                availabilityDate.barn_booking_status = "FR"
                            else:
                                logger.error("Status for Barn should have been changeover or booked PM: " + str(availabilityDate))
                                raise ValueError("Booking status incorrect")
                        else:
                            logger.error("Property(" + str(old_property) + ") not valid")
                            raise ValueError("Invalid Property")
                    # Old Middle date: (Booked -> Free) else error
                    else:
                        if str(self.original_property) == "Cottage":
                            if str(availabilityDate.cottage_booking_status) == "BK":
                                availabilityDate.cottage_booking_status = "FR"
                            else:
                                logger.error("Status for Cottage should have been booked: " + str(availabilityDate))
                                raise ValueError("Booking status incorrect")
                        elif str(self.original_property) == "Barn":
                            if str(availabilityDate.barn_booking_status) == "BK":
                                availabilityDate.barn_booking_status = "FR"
                            else:
                                logger.error("Status for Barn should have been booked: " + str(availabilityDate))
                                raise ValueError("Booking status incorrect")
                        else:
                            logger.error("Property(" + str(old_property) + ") not valid")
                            raise ValueError("Invalid Property")
                    booking.dates.add(availabilityDate)
                    availabilityDate.save()

                # sort end date
                availabilityDate = AvailabilityDate.objects.get(date=self.original_end_date)

                # Old End date: (Changeover -> Booked PM) OR (Booked AM -> Free) else error
                if str(self.original_property) == "Cottage":
                    if str(availabilityDate.cottage_booking_status) == "CH":
                        availabilityDate.cottage_booking_status = "PM"
                    elif str(availabilityDate.cottage_booking_status) == "AM":
                        availabilityDate.cottage_booking_status = "FR"
                    else:
                        logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
                        raise ValueError("Booking status incorrect")
                elif str(self.original_property) == "Barn":
                    if str(availabilityDate.barn_booking_status) == "CH":
                        availabilityDate.barn_booking_status = "PM"
                    elif str(availabilityDate.barn_booking_status) == "AM":
                        availabilityDate.barn_booking_status = "FR"
                    else:
                        logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
                        raise ValueError("Booking status incorrect")
                booking.dates.add(availabilityDate)
                availabilityDate.save()


            # clear the old dates from the booking - if there are any
            booking.dates.clear()


            # create new 'AvailabilityDate's if needed, set/update booking status and link to the booking
            for bookingDate in daterange(self.instance.start_date, self.instance.end_date):
                availabilityDate, created = AvailabilityDate.objects.get_or_create(date=bookingDate)
                logger.error("Created(" + str(created) + ") date: " + str(availabilityDate))
                # Start date: (Booked AM -> Changeover) OR (Free -> Booked PM) else error
                if bookingDate == self.instance.start_date:
                    if self.instance.property.name == "Cottage":
                        logger.error("Cottage booking status changing from " + str(availabilityDate.cottage_booking_status))
                        if str(availabilityDate.cottage_booking_status) == "AM":
                            availabilityDate.cottage_booking_status = "CH"
                        elif str(availabilityDate.cottage_booking_status) == "FR":
                            availabilityDate.cottage_booking_status = "PM"
                            logger.error("Cottage booking status changing to " + str(availabilityDate.cottage_booking_status))
                        else:
                            logger.error("Status for Cottage should have been free or booked AM: " + str(availabilityDate))
                            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
                    elif self.instance.property.name == "Barn":
                        if str(availabilityDate.barn_booking_status) == "AM":
                            availabilityDate.barn_booking_status = "CH"
                        elif str(availabilityDate.barn_booking_status) == "FR":
                            availabilityDate.barn_booking_status = "PM"
                        else:
                            logger.error("Status for Barn should have been free or booked AM: " + str(availabilityDate))
                            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
                    else:
                        logger.error("Property(" + str(old_property) + ") not valid")
                        raise ValueError("Invalid Property")
                # Middle date: (Free -> Booked) else error
                else:
                    if self.instance.property.name == "Cottage":
                        if str(availabilityDate.cottage_booking_status) == "FR":
                            availabilityDate.cottage_booking_status = "BK"
                        else:
                            logger.error("Status for Cottage should have been free: " + str(availabilityDate))
                            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
                    elif self.instance.property.name == "Barn":
                        if str(availabilityDate.barn_booking_status) == "FR":
                            availabilityDate.barn_booking_status = "BK"
                        else:
                            logger.error("Status for Barn should have been free: " + str(availabilityDate))
                            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
                    else:
                        logger.error("Property(" + str(old_property) + ") not valid")
                        raise ValueError("Invalid Property")
                booking.dates.add(availabilityDate)
                availabilityDate.save()

            # sort end date
            availabilityDate, created = AvailabilityDate.objects.get_or_create(date=self.instance.end_date)
            logger.error("Created(" + str(created) + ") date: " + str(availabilityDate))
            # End date: (Booked PM -> Changeover) OR (Free -> Booked AM) else error
            if self.instance.property.name == "Cottage":
                if str(availabilityDate.cottage_booking_status) == "PM":
                    availabilityDate.cottage_booking_status = "CH"
                elif str(availabilityDate.cottage_booking_status) == "FR":
                    availabilityDate.cottage_booking_status = "AM"
                else:
                    logger.error("Status for Cottage should have been free or booked PM: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            elif self.instance.property.name == "Barn":
                if str(availabilityDate.barn_booking_status) == "PM":
                    availabilityDate.barn_booking_status = "CH"
                elif str(availabilityDate.barn_booking_status) == "FR":
                    availabilityDate.barn_booking_status = "AM"
                else:
                    logger.error("Status for Cottage should have been free or booked PM: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            booking.dates.add(availabilityDate)
            availabilityDate.save()

            booking.save()

        else:
            logger.error("No change")

        return booking


class BookingAdmin(admin.ModelAdmin):
    exclude = ('dates',)
    form = BookingForm
    list_display = ('property', 'start_date', 'end_date', 'customer_name')
    list_filter = ('property', 'start_date',)

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'cottage_booking_status', 'barn_booking_status', 'cottage_week_price', 'barn_week_price')
    list_filter = ('date', 'cottage_booking_status', 'barn_booking_status',)

class PricingPeriodAdmin(admin.ModelAdmin):
    exclude = ('dates',)
    form = PricingPeriodForm
    list_display = ('property', 'start_date', 'end_date', 'price')
    list_filter = ('property', 'start_date',)


# Catch signal when a pricing period is about to be deleted
@receiver(pre_delete, sender=PricingPeriod)
def delete_pricing_period(sender, instance, **kwargs):
    logger = logging.getLogger(__name__)
    logger.error("About to delete a pricing period: " + str(instance))


# Catch signal when a booking is about to be deleted
@receiver(pre_delete, sender=Booking)
def delete_booking(sender, instance, **kwargs):
    logger = logging.getLogger(__name__)
    logger.error("About to delete a booking: " + str(instance))

    # clear the property from the old dates - if there are any
    # Revert booking status on all 'AvailabilityDate's
    for oldBookingDate in daterange(instance.start_date, instance.end_date):
        availabilityDate = AvailabilityDate.objects.get(date=oldBookingDate)

        # Old Start date: (Changeover -> Booked AM) OR (Booked PM -> Free) else error
        if oldBookingDate == instance.start_date:
            if instance.property.name == "Cottage":
                logger.error("Cottage booking status changing from " + str(availabilityDate.cottage_booking_status))
                if str(availabilityDate.cottage_booking_status) == "CH":
                    availabilityDate.cottage_booking_status = "AM"
                elif str(availabilityDate.cottage_booking_status) == "PM":
                    availabilityDate.cottage_booking_status = "FR"
                else:
                    logger.error("Status for Cottage should have been changeover or booked PM: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            elif instance.property.name == "Barn":
                if str(availabilityDate.barn_booking_status) == "CH":
                    availabilityDate.barn_booking_status = "AM"
                elif str(availabilityDate.barn_booking_status) == "PM":
                    availabilityDate.barn_booking_status = "FR"
                else:
                    logger.error("Status for Barn should have been changeover or booked PM: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            else:
                logger.error("Property(" + str(old_property) + ") not valid")
                raise ValueError("Invalid Property")
        # Old Middle date: (Booked -> Free) else error
        else:
            if instance.property.name == "Cottage":
                if str(availabilityDate.cottage_booking_status) == "BK":
                    availabilityDate.cottage_booking_status = "FR"
                else:
                    logger.error("Status for Cottage should have been booked: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            elif instance.property.name == "Barn":
                if str(availabilityDate.barn_booking_status) == "BK":
                    availabilityDate.barn_booking_status = "FR"
                else:
                    logger.error("Status for Barn should have been booked: " + str(availabilityDate))
                    raise ValueError("Booking status incorrect")
            else:
                logger.error("Property(" + str(old_property) + ") not valid")
                raise ValueError("Invalid Property")
        availabilityDate.save()

    # sort end date
    availabilityDate = AvailabilityDate.objects.get(date=instance.end_date)

    # Old End date: (Changeover -> Booked PM) OR (Booked AM -> Free) else error
    if instance.property.name == "Cottage":
        if str(availabilityDate.cottage_booking_status) == "CH":
            availabilityDate.cottage_booking_status = "PM"
        elif str(availabilityDate.cottage_booking_status) == "AM":
            availabilityDate.cottage_booking_status = "FR"
        else:
            logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    elif instance.property.name == "Barn":
        if str(availabilityDate.barn_booking_status) == "CH":
            availabilityDate.barn_booking_status = "PM"
        elif str(availabilityDate.barn_booking_status) == "AM":
            availabilityDate.barn_booking_status = "FR"
        else:
            logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    availabilityDate.save()

    # clear the old dates from the booking - if there are any
    instance.dates.clear()



# Register your models here.
admin.site.register(AvailabilityDate, AvailabilityAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Property)
admin.site.register(PricingPeriod, PricingPeriodAdmin)
