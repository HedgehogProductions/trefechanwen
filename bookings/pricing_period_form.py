from django import forms
import logging

from django.db.models.signals import pre_delete

from django.dispatch import receiver

from .models import PricingPeriod

from .form_helpers import daterange, set_week_price

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
        self.original_price = self.instance.price

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
            ", property from: " + str(self.original_property) + " to: " + str(self.cleaned_data.get('property')) +
            " and price from: " + str(self.original_price) + " to: " + str(self.cleaned_data.get('price')))

            # clear the property price from the old dates - if there are any
            if self.original_start_date != None and self.original_end_date != None and self.original_property != None :
                logger.error("removing old dates from " + str(self.original_property))
                # Revert price to None on all 'AvailabilityDate's
                for oldDate in daterange(self.original_start_date, self.original_end_date):
                    set_week_price(oldDate, self.original_property, None, False)

                # sort end date
                set_week_price(self.original_end_date, self.original_property, None, False)

            # clear the old dates from the PricingPeriod - if there are any
            pricing_period.dates.clear()

            # create new AvailabilityDates if needed, set the price and add to the PricingPeriod
            for newDate in daterange(self.instance.start_date, self.instance.end_date):
                availabilityDate = set_week_price(newDate, self.instance.property, self.instance.price, self.instance.discount)
                pricing_period.dates.add(availabilityDate)

            # sort end date
            availabilityDate = set_week_price(self.instance.end_date, self.instance.property, self.instance.price, self.instance.discount)
            pricing_period.dates.add(availabilityDate)

            pricing_period.save()


        else:
            logger.error("No change")

        return pricing_period


# Catch signal when a pricing period is about to be deleted
@receiver(pre_delete, sender=PricingPeriod)
def delete_pricing_period(sender, instance, **kwargs):
    logger = logging.getLogger(__name__)
    logger.error("About to delete a pricing period: " + str(instance))

    # clear the property price from the old dates - if there are any
    if instance.original_start_date != None and instance.original_end_date != None and instance.original_property != None :
        logger.error("removing old dates from " + str(instance.original_property))
        # Revert price to None on all 'AvailabilityDate's
        for oldDate in daterange(instance.start_date, instance.end_date):
            set_week_price(oldDate, instance.property, None, False)

        # sort end date
        set_week_price(instance.end_date, instance.property, None, False)

    # clear the old dates from the PricingPeriod - if there are any
    instance.dates.clear()