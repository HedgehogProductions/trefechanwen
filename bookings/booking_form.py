from django import forms
from datetime import date
import logging

from django.db.models.signals import pre_delete

from django.dispatch import receiver

from .models import Booking, AvailabilityDate
from .form_helpers import daterange, change_booking_status, cancel_pm_booking, make_pm_booking, cancel_am_booking, make_am_booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
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
        booking = super(BookingForm, self).save(commit=False)
        booking.save()

        # if the dates or property has changed:
        if self.changed_data:
            logger.debug("Changing dates from: " + str(self.original_start_date) + " - " + str(self.original_end_date) +
            " to: " + str(self.cleaned_data.get('start_date')) + " - " + str(self.cleaned_data.get('end_date')) +
            " and property from: " + str(self.original_property) + " to: " + str(self.cleaned_data.get('property')))

            # clear the property from the old dates - if there are any
            if self.original_start_date != None and self.original_end_date != None and self.original_property != None:
                logger.debug("removing old dates from " + str(self.original_property))
                # Revert booking status on all 'AvailabilityDate's
                for oldDate in daterange(self.original_start_date, self.original_end_date):
                    if oldDate == self.original_start_date:
                        cancel_pm_booking(oldDate, self.original_property)
                    else:
                        change_booking_status(oldDate, self.original_property, "BK", "FR")

                # sort end date
                cancel_am_booking(self.original_end_date, self.original_property)

            # clear the old dates from the booking - if there are any
            booking.dates.clear()

            # create new 'AvailabilityDate's if needed, set/update booking status and add to the Booking
            logger.debug("Adding new dates to " + str(self.instance.property.name))
            for newDate in daterange(self.instance.start_date, self.instance.end_date):
                logger.debug("Adding " + str(newDate))
                if newDate == self.instance.start_date:
                    availabilityDate = make_pm_booking(newDate, self.instance.property.name)
                    booking.dates.add(availabilityDate)
                else:
                    availabilityDate = change_booking_status(newDate, self.instance.property.name, "FR", "BK")
                    booking.dates.add(availabilityDate)

            # sort end date
            logger.debug("Adding " + str(self.instance.end_date))
            availabilityDate = make_am_booking(self.instance.end_date, self.instance.property.name)
            booking.dates.add(availabilityDate)

            booking.save()

        else:
            logger.debug("No change")

        return booking



# Catch signal when a booking is about to be deleted
@receiver(pre_delete, sender=Booking)
def delete_booking(sender, instance, **kwargs):
    logger = logging.getLogger(__name__)

    # clear the property from the old dates - if there are any
    if instance.start_date != None and instance.end_date != None and instance.property != None:
        logger.debug("removing old dates from " + str(instance.property))
        # Revert booking status on all 'AvailabilityDate's
        for oldDate in daterange(instance.start_date, instance.end_date):
            if oldDate == instance.start_date:
                cancel_pm_booking(oldDate, instance.property)
            else:
                change_booking_status(oldDate, instance.property, "BK", "FR")

        # sort end date
        cancel_am_booking(instance.end_date, instance.property)

    # clear the old dates from the booking - if there are any
    instance.dates.clear()
