
// Types of bookings
var BookingType = {
    NONE: 0,
    ALL: 1,
    AM: 2,
    PM: 3,
};

// Get last day of the month
function daysInMonth(month, year) {
    // Add one to month to get next month, then set day to 0 (the day before the 1st)
    return new Date(year, month+1, 0).getDate();
}

// Get the html for a calendar cell with given text
function getCellHtml(content, bookingType) {
    var cellHtmlClass = ""
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
    return "<td class=\"availability-calendar-day" + cellHtmlClass + "\"><a class=\"availability-calendar-text\" href=\"#\">" + content + "</a></td>";
}
function getEmptyCellHtml(content) {
    return "<td class=\"availability-calendar-day empty-day\"><a class=\"availability-calendar-text\" href=\"#\">" + content + "</a></td>";
}

// Extract dates booked between two dates from database results
function getBookedDates(firstDay, lastDay, xmlHttpResults) {
    var bookings = {};
    console.log("getBookedDates");
    var bookingsJson = JSON.parse(xmlHttpResults);
    console.log("looking at " + bookingsJson.results.length + " bookings");
    for (var bookingNumber =0; bookingNumber < bookingsJson.results.length; ++bookingNumber) {
        var startDate = new Date(bookingsJson.results[bookingNumber].start_date);
        var endDate = new Date(bookingsJson.results[bookingNumber].end_date);
        var bookingLength = endDate - startDate;
        console.log("Got booking for " + startDate.toISOString() + " to " + endDate.toISOString() + "(" + bookingLength + " days)");
        if ( startDate >= firstDay ) {
            bookings[startDate.getDate()] = BookingType.PM;
        }
        if ( endDate <= lastDay ) {
            bookings[endDate.getDate()] = BookingType.AM;
        }
        // for (var fullDay = startDate.getDate()+1; fullDay < endDate && fullDay <= lastDay; startDate.setDate(startDate.getDate + 1)) {
        //     if (fullDay >= firstDay) {
        //         bookings[fullDay.getDate()] = BookingType.ALL;
        //     }
        // }

    }

    return bookings;
}

// Build HTML for month calendar view
function getMonthHtml(month, year, xmlHttpResults) {
    var firstDayOfMonth = new Date(year, month, 1);
    var lastDayOfMonth = daysInMonth(month, year);
    var bookedDates = getBookedDates(firstDayOfMonth, lastDayOfMonth, xmlHttpResults);
    console.log("Booked on: " + bookedDates);

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
        monthHtml += getCellHtml(dayOfMonth.toString(), bookedDates[dayOfMonth]);
        if ((dayOfMonth + emptyCells) % 7 === 0) {
            monthHtml += "</tr>";
        }
    }
    monthHtml += "</tr></tbody></table>";
    return monthHtml;
}

function updateMonthView(viewId, xmlHttpResults) {
    var currentMonth = document.getElementById(viewId).getAttribute("month");
    var currentYear = document.getElementById(viewId).getAttribute("year");
    var firstDayOfMonth = new Date(currentYear, currentMonth, 1);

    document.getElementById(viewId).innerHTML = getMonthHtml(firstDayOfMonth.getMonth(), firstDayOfMonth.getFullYear(), xmlHttpResults);
}

function changeAllMonths(monthChange) {
    // Update attributes to new months
    var currentMonth = document.getElementById("availabilityCalendarCottageMonth1").getAttribute("month");
    var currentYear = document.getElementById("availabilityCalendarCottageMonth1").getAttribute("year");
    var firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    firstDayOfMonth.setMonth(firstDayOfMonth.getMonth() + monthChange);
    var firstDayOfNextMonth = new Date(firstDayOfMonth);
    firstDayOfNextMonth.setMonth(firstDayOfNextMonth.getMonth()+1);

    document.getElementById("availabilityCalendarCottageMonth1").setAttribute("month", firstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendarCottageMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
    document.getElementById("availabilityCalendarCottageMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
    document.getElementById("availabilityCalendarCottageMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());
    document.getElementById("availabilityCalendarBarnMonth1").setAttribute("month", firstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendarBarnMonth1").setAttribute("year", firstDayOfMonth.getFullYear());
    document.getElementById("availabilityCalendarBarnMonth2").setAttribute("month", firstDayOfNextMonth.getMonth());
    document.getElementById("availabilityCalendarBarnMonth2").setAttribute("year", firstDayOfNextMonth.getFullYear());

    // Get availability data and use to update html
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Got bookings: " + this.responseText);
            updateMonthView("availabilityCalendarCottageMonth1", this.responseText);
            updateMonthView("availabilityCalendarCottageMonth2", this.responseText);
            updateMonthView("availabilityCalendarBarnMonth1", this.responseText);
            updateMonthView("availabilityCalendarBarnMonth2", this.responseText);
        }
    };
    xhttp.open("GET", "/bookings/", true);
    xhttp.send();
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