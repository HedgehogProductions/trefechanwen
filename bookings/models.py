from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class AvailabilityDate(models.Model):

    BOOKING_TYPE_CHOICES = (
        ('FR', 'free'),
        ('BK', 'booked'),
        ('AM', 'bookedAm'),
        ('PM', 'bookedPm'),
        ('CH', 'changeOver'),
    )

    # Fields
    date = models.DateField(primary_key=True)
    cottage_booking_status = models.CharField(max_length=2, choices=BOOKING_TYPE_CHOICES, default='FR')
    barn_booking_status = models.CharField(max_length=2, choices=BOOKING_TYPE_CHOICES, default='FR')
    cottage_week_price = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    barn_week_price = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    cottage_week_price_discount = models.BooleanField(default=False)
    barn_week_price_discount = models.BooleanField(default=False)


    # Metadata
    class Meta:
        ordering = ["date"]


    # Methods
    def get_absolute_url(self):
             """
             Returns the url to access a particular instance of MyModelName.
             """
             return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
         return '%s - Cottage(%s), Barn(%s)' % (self.date,self.cottage_booking_status,self.barn_booking_status)


class Booking(models.Model):

    # Fields
    property = models.ForeignKey(
        'Property',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=20, help_text="Enter the name of the customer")
    dates = models.ManyToManyField(AvailabilityDate)


    # Metadata
    class Meta:
        ordering = ["start_date"]


    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return '%s(%s - %s): %s' % (self.property.name,self.start_date,self.end_date,self.customer_name)



class Property(models.Model):

    # Fields
    name = models.CharField(primary_key=True, max_length=20, help_text="The name of the property")


    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.name



class PricingPeriod(models.Model):

    # Fields
    property = models.ForeignKey(
        'Property',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=4, decimal_places=0, validators=[MinValueValidator(Decimal('0'))],
                                help_text="Enter the full-week price - e.g. 660")
    discount = models.BooleanField(default=False, help_text="Select to mark price as discounted")
    dates = models.ManyToManyField(AvailabilityDate)


    # Metadata
    class Meta:
        ordering = ["start_date"]


    # Methods
    def get_absolute_url(self):
         """
         Returns the url to access a particular instance of MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return '%s(%s - %s): £%s' % (self.property.name,self.start_date,self.end_date,self.price)