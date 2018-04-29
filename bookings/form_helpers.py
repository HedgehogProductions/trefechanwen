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
            raise ValueError("Cottage already has a price set for: " + str(availabilityDate))
        availabilityDate.cottage_week_price = price
        availabilityDate.cottage_week_price_discount = discount
    elif str(property) == "Barn":
        if price != None and availabilityDate.barn_week_price != None:
            logger.error("Barn already has a price set for: " + str(availabilityDate))
            raise ValueError("Barn already has a price set for: " + str(availabilityDate))
        availabilityDate.barn_week_price = price
        availabilityDate.barn_week_price_discount = discount
    else:
        logger.error("Property(" + str(old_property) + ") not valid")
        raise ValueError("Property(" + str(old_property) + ") not valid")
    availabilityDate.save()

    return availabilityDate


def cancel_pm_booking(date, property):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    # Old Start date: (Changeover -> Booked AM) OR (Booked PM -> Free) else error
    if str(property) == "Cottage":
        if str(availabilityDate.cottage_booking_status) == "CH":
            availabilityDate.cottage_booking_status = "AM"
        elif str(availabilityDate.cottage_booking_status) == "PM":
            availabilityDate.cottage_booking_status = "FR"
        else:
            logger.error("Status for Cottage should have been changeover or booked PM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    elif str(property) == "Barn":
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
    availabilityDate.save()

    return availabilityDate


def make_pm_booking(date, property):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    # Start date: (Booked AM -> Changeover) OR (Free -> Booked PM) else error
    if str(property) == "Cottage":
        if str(availabilityDate.cottage_booking_status) == "AM":
            availabilityDate.cottage_booking_status = "CH"
        elif str(availabilityDate.cottage_booking_status) == "FR":
            availabilityDate.cottage_booking_status = "PM"
        else:
            logger.error("Status for Cottage should have been free or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
    elif str(property) == "Barn":
        if str(availabilityDate.barn_booking_status) == "AM":
            availabilityDate.barn_booking_status = "CH"
        elif str(availabilityDate.barn_booking_status) == "FR":
            availabilityDate.barn_booking_status = "PM"
        else:
            logger.error("Status for Barn should have been free or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect - is the property already booked on " + str(availabilityDate.date) + "?")
    else:
        logger.error("Property(" + str(property) + ") not valid")
        raise ValueError("Invalid Property")
    availabilityDate.save()

    return availabilityDate


def change_booking_status(date, property, from_status, to_status):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    error_string = "Booking status incorrect"
    if str(from_status) == "FR":
        error_string = "Booking status incorrect - is the " + str(property) + " already booked on " + str(availabilityDate.date) + "?"

    if str(property) == "Cottage":
        if str(availabilityDate.cottage_booking_status) == str(from_status):
            availabilityDate.cottage_booking_status = str(to_status)
        else:
            logger.error("Status for Cottage should have been " + str(from_status) + ": " + str(availabilityDate))
            raise ValueError(error_string)
    elif str(property) == "Barn":
        if str(availabilityDate.barn_booking_status) == str(from_status):
            availabilityDate.barn_booking_status = str(to_status)
        else:
            logger.error("Status for Barn should have been " + str(from_status) + ": " + str(availabilityDate))
            raise ValueError(error_string)
    else:
        logger.error("Property(" + str(old_property) + ") not valid")
        raise ValueError("Invalid Property")
    availabilityDate.save()

    return availabilityDate


def cancel_am_booking(date, property):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    # Old End date: (Changeover -> Booked PM) OR (Booked AM -> Free) else error
    if str(property) == "Cottage":
        if str(availabilityDate.cottage_booking_status) == "CH":
            availabilityDate.cottage_booking_status = "PM"
        elif str(availabilityDate.cottage_booking_status) == "AM":
            availabilityDate.cottage_booking_status = "FR"
        else:
            logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    elif str(property) == "Barn":
        if str(availabilityDate.barn_booking_status) == "CH":
            availabilityDate.barn_booking_status = "PM"
        elif str(availabilityDate.barn_booking_status) == "AM":
            availabilityDate.barn_booking_status = "FR"
        else:
            logger.error("Status for Cottage should have been changeover or booked AM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    availabilityDate.save()

    return availabilityDate


def make_am_booking(date, property):
    logger = logging.getLogger(__name__)
    availabilityDate, created = AvailabilityDate.objects.get_or_create(date=date)

    # End date: (Booked PM -> Changeover) OR (Free -> Booked AM) else error
    if str(property) == "Cottage":
        if str(availabilityDate.cottage_booking_status) == "PM":
            availabilityDate.cottage_booking_status = "CH"
        elif str(availabilityDate.cottage_booking_status) == "FR":
            availabilityDate.cottage_booking_status = "AM"
        else:
            logger.error("Status for Cottage should have been free or booked PM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    elif str(property) == "Barn":
        if str(availabilityDate.barn_booking_status) == "PM":
            availabilityDate.barn_booking_status = "CH"
        elif str(availabilityDate.barn_booking_status) == "FR":
            availabilityDate.barn_booking_status = "AM"
        else:
            logger.error("Status for Cottage should have been free or booked PM: " + str(availabilityDate))
            raise ValueError("Booking status incorrect")
    availabilityDate.save()

    return availabilityDate
