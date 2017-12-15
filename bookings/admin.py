from django.contrib import admin

# Register your models here.
from .models import Booking, Property

admin.site.register(Booking)
admin.site.register(Property)