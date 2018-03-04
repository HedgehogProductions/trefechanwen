from django import forms
import logging

from django.db.models.signals import pre_delete

from django.dispatch import receiver

from .models import PricingPeriod

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

# Catch signal when a pricing period is about to be deleted
@receiver(pre_delete, sender=PricingPeriod)
def delete_pricing_period(sender, instance, **kwargs):
    logger = logging.getLogger(__name__)
    logger.error("About to delete a pricing period: " + str(instance))
