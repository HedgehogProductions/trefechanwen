import logging

from datetime import timedelta

from .models import AvailabilityDate

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def set_week_price(date, property, price, discount):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    if str(property) == "Cottage":
        if price != None and availabilityDate.cottage_week_price != None:
            logger.error("Cottage already has a price set for: " + str(availabilityDate))
            raise ValueError("Price already set")
        availabilityDate.cottage_week_price = price
        availabilityDate.cottage_week_price_discount = discount
    elif str(property) == "Barn":
        if price != None and availabilityDate.barn_week_price != None:
            logger.error("Barn already has a price set for: " + str(availabilityDate))
            raise ValueError("Price already set")
        availabilityDate.barn_week_price = price
        availabilityDate.barn_week_price_discount = discount
    else:
        logger.error("Property(" + str(old_property) + ") not valid")
        raise ValueError("Invalid Property")
    availabilityDate.save()

    return availabilityDate
