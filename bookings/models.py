from django.db import models

class Booking(models.Model):

    # Fields
    property = models.ForeignKey(
        'Property',
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=20, help_text="Enter the name of the customer")


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