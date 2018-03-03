
// Types of bookings
var BookingType = {
    NONE: 0,
    ALL: 1,
    AM: 2,
    PM: 3
};

var Property = {
    COTTAGE: 0,
    BARN: 1
};

// Get last day of the month
function daysInMonth(month, year) {
    // Add one to month to get next month, then set day to 0 (the day before the 1st)
    return new Date(year, month+1, 0).getDate();
}

// Get the html for a calendar cell with given text
function getCellHtml(content, bookingType) {
    var cellHtmlClass = "";
    switch(bookingType) {
        case BookingType.ALL:
            cellHtmlClass = " availability-full";
            break;
        case BookingType.AM:
            cellHtmlClass = " availability-pm";
            break;
        case BookingType.PM:
            cellHtmlClass = " availability-am";
            break;
        default:
    }
    return "<td class=\"availability-calendar-day" + cellHtmlClass + "\"><a class=\"availability-calendar-text-container\" href=\"#\"></a>" +
        "<div class=\"availability-calendar-text\">" + content + "</div></td>";
}
function getEmptyCellHtml(content) {
    return "<td class=\"availability-calendar-day empty-day\"><a class=\"availability-calendar-text-container\" href=\"#\"></a>" +
        "<div class=\"availability-calendar-text\">" + content + "</div></td>";
}

// Extract dates booked from database results, given a property and month
function getBookedDates(property, xmlHttpResults) {
    var bookings = new Map();
    var bookingStatus = BookingType.NONE;
    var datesJson = JSON.parse(xmlHttpResults);
    for (var dateNumber = 0; dateNumber < datesJson.results.length; ++dateNumber) {
        var date = new Date(datesJson.results[dateNumber].date);
        //var bookingsSet = datesJson.results[date]
        switch(property) {
            case Property.COTTAGE:
                booking_status = datesJson.results[dateNumber].cottage_booking_status;
                break;
            case Property.BARN:
                booking_status = datesJson.results[dateNumber].barn_booking_status;
                break;
            default:
                console.error("Cannot get booked dates for unknown property " + property);
        }
        switch(booking_status) {
            case "FR":
                break;
            case "CH":
            case "BK":
                bookings.set(date.getDate(), BookingType.ALL);
                break;
            case "AM":
                bookings.set(date.getDate(), BookingType.AM);
                break;
            case "PM":
                bookings.set(date.getDate(), BookingType.PM);
                break;
            default:
                console.error("Cannot handle unknown booking status " + bookingStatus + " on " + date.toISOString());
        }
    }
    return bookings;
}

// Build HTML for month calendar view
function getMonthHtml(month, year, property, xmlHttpResults) {
    var firstDayOfMonth = new Date(year, month, 1);
    var bookedDates = getBookedDates(property, xmlHttpResults);

    var monthHtml = "";

    // Set up strings for later
    var monthStrings = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    var dayHeaderNames = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

    // Build month header
    var yearString = firstDayOfMonth.getFullYear().toString();
    var monthString = monthStrings[firstDayOfMonth.getMonth()];
    monthHtml += "<div class=\"availability-calendar-title\">" + monthString + " " + yearString + "</div>";

    // Build column headers
    var weekHeaders = "<table class=\"availability-calendar-month\"><thead><tr>";
    for (var day in dayHeaderNames) {
        weekHeaders += "<th>";
        weekHeaders += dayHeaderNames[day];
        weekHeaders += "</th>";
    }
    weekHeaders += "</tr></thead>";

    monthHtml += weekHeaders;
    monthHtml += "<tbody><tr>";
    var emptyCells = firstDayOfMonth.getDay();
    for (var emptyCell = 0; emptyCell < emptyCells; emptyCell++) {
        monthHtml += getEmptyCellHtml("");
    }
    var daysInThisMonth = daysInMonth(firstDayOfMonth.getMonth(), firstDayOfMonth.getFullYear());
    for (var dayOfMonth = 1;
         dayOfMonth <= daysInThisMonth;
         dayOfMonth++) {
        if ((dayOfMonth + emptyCells) % 7 === 1) {
            monthHtml += "<tr>";
        }
        monthHtml += getCellHtml(dayOfMonth.toString(), bookedDates.get(dayOfMonth));
        if ((dayOfMonth + emptyCells) % 7 === 0) {
            monthHtml += "</tr>";
        }
    }
    monthHtml += "</tr></tbody></table>";
    return monthHtml;
}

function updateMonthView(viewId, property, xmlHttpResults) {
    var currentMonth = document.getElementById(viewId).getAttribute("month");
    var currentYear = document.getElementById(viewId).getAttribute("year");
    var firstDayOfMonth = new Date(currentYear, currentMonth, 1);

    document.getElementById(viewId).innerHTML = getMonthHtml(firstDayOfMonth.getMonth(), firstDayOfMonth.getFullYear(), property, xmlHttpResults);
}

function changeAllMonths(monthChange) {
    // Update attributes to new months
    var currentMonth = document.getElementById("availabilityCalendarCottageMonth1").getAttribute("month");
    var currentYear = document.getElementById("availabilityCalendarCottageMonth1").getAttribute("year");

    var firstDayOfMonth = new Date(currentYear, currentMonth, 1, 1, 0, 0, 0);
    firstDayOfMonth.setMonth(firstDayOfMonth.getMonth() + monthChange);

    var firstDayOfNextMonth = new Date(firstDayOfMonth);
    firstDayOfNextMonth.setMonth(firstDayOfNextMonth.getMonth()+1);

    var lastDayOfMonth = new Date(firstDayOfNextMonth);
    lastDayOfMonth.setDate(lastDayOfMonth.getDate()-1);

    var lastDayOfNextMonth = new Date(firstDayOfNextMonth);
    lastDayOfNextMonth.setMonth(lastDayOfNextMonth.getMonth()+1);
    lastDayOfNextMonth.setDate(lastDayOfNextMonth.getDate()-1);

    document.getElementById("availabilityCalendarCottageMonth1").setAttribute("month", firstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendarCottageMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
    document.getElementById("availabilityCalendarCottageMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
    document.getElementById("availabilityCalendarCottageMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());
    document.getElementById("availabilityCalendarBarnMonth1").setAttribute("month", firstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendarBarnMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
    document.getElementById("availabilityCalendarBarnMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
    document.getElementById("availabilityCalendarBarnMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());

    // Get availability data and use to update html
    var urlParamsMonth1 = "/availabilitydates/?format=json&limit=100&start_date="
        + firstDayOfMonth.toISOString().substring(0,10) + "&end_date=" + lastDayOfMonth.toISOString().substring(0,10);
    var urlParamsMonth2 = "/availabilitydates/?format=json&limit=100&start_date="
        + firstDayOfNextMonth.toISOString().substring(0,10) + "&end_date=" + lastDayOfNextMonth.toISOString().substring(0,10);
    var xhttpRequestMonth1 = new XMLHttpRequest();
    var xhttpRequestMonth2 = new XMLHttpRequest();
    xhttpRequestMonth1.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            updateMonthView("availabilityCalendarCottageMonth1", Property.COTTAGE, this.responseText);
            updateMonthView("availabilityCalendarBarnMonth1", Property.BARN, this.responseText);
        }
    };
    xhttpRequestMonth2.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            updateMonthView("availabilityCalendarCottageMonth2", Property.COTTAGE, this.responseText);
            updateMonthView("availabilityCalendarBarnMonth2", Property.BARN, this.responseText);
        }
    };
    xhttpRequestMonth1.open("GET", urlParamsMonth1, true);
    xhttpRequestMonth1.send();
    xhttpRequestMonth2.open("GET", urlParamsMonth2, true);
    xhttpRequestMonth2.send();
}

function showNextMonth() {
    changeAllMonths(1);
}

function showPreviousMonth() {
    changeAllMonths(-1);
}


// Find current and next month
var firstDayOfMonth = new Date();
firstDayOfMonth.setDate(1);
var firstDayOfNextMonth = new Date();
firstDayOfNextMonth.setDate(1);
firstDayOfNextMonth.setMonth(firstDayOfMonth.getMonth()+1);

document.getElementById("lastMonthCottage").onclick = showPreviousMonth;
document.getElementById("nextMonthCottage").onclick = showNextMonth;
document.getElementById("lastMonthBarn").onclick = showPreviousMonth;
document.getElementById("nextMonthBarn").onclick = showNextMonth;

document.getElementById("availabilityCalendarCottageMonth1").setAttribute("month", firstDayOfMonth.getMonth());
document.getElementById("availabilityCalendarCottageMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
document.getElementById("availabilityCalendarCottageMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
document.getElementById("availabilityCalendarCottageMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());
document.getElementById("availabilityCalendarBarnMonth1").setAttribute("month", firstDayOfMonth.getMonth());
document.getElementById("availabilityCalendarBarnMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
document.getElementById("availabilityCalendarBarnMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
document.getElementById("availabilityCalendarBarnMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());

changeAllMonths(0);