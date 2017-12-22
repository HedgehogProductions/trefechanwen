
// Get last day of the month
function daysInMonth(month, year) {
    // Add one to month to get next month, then set day to 0 (the day before the 1st)
    return new Date(year, month+1, 0).getDate();
}

// Get the html for a calendar cell with given text
function getCellHtml(content) {
    return "<td class=\"availability-calendar-day\">" + content + "</td>";
}

// Build HTML for month calendar view
function getMonthHtml(month, year) {
    var monthHtml = "<div class=\"mdl-cell mdl-cell--4-col\"><div class=\"availabilty-calendar-month\">";

    // Set up strings for later
    var monthStrings = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    var dayHeaderNames = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

    // Build month header
    var firstDayOfMonth = new Date(year, month, 1);
    var yearString = firstDayOfMonth.getFullYear().toString();
    var monthString = monthStrings[firstDayOfMonth.getMonth()];
    monthHtml += "<div class=\"availability-calendar-title\">" + monthString + " " + yearString + "</div>";

    // Build column headers
    var weekHeaders = "<table class=\"availability-calendar-day\"><thead><tr>";
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
        monthHtml += getCellHtml("");
    }
    var daysInThisMonth = daysInMonth(firstDayOfMonth.getMonth(), firstDayOfMonth.getFullYear());
    for (var dayOfMonth = 1;
         dayOfMonth <= daysInThisMonth;
         dayOfMonth++) {
        if ((dayOfMonth + emptyCells) % 7 === 1) {
            monthHtml += "<tr>";
        }
        monthHtml += getCellHtml(dayOfMonth.toString());
        if ((dayOfMonth + emptyCells) % 7 === 0) {
            monthHtml += "</tr>";
        }
    }
    monthHtml += "</tr></tbody></table></div></div>";
    return monthHtml;
}

// Build html for complete calendar view
function getCalendarHtml(startMonth, startYear) {
    var currentCalendarHtml = getMonthHtml(startMonth, startYear);

    var firstDayOfNextMonth = new Date(startYear, startMonth, 1);
    firstDayOfNextMonth.setMonth(firstDayOfNextMonth.getMonth()+1);

    currentCalendarHtml += getMonthHtml(firstDayOfNextMonth.getMonth(),
                                        firstDayOfNextMonth.getFullYear())

    return currentCalendarHtml;
}

function showPreviousMonth() {
    // Get current month and decrement
    var currentMonth = document.getElementById("availabilityCalendar").getAttribute("month");
    var currentYear = document.getElementById("availabilityCalendar").getAttribute("year");
    var newFirstDayOfMonth = new Date(currentYear, currentMonth, 1);
    newFirstDayOfMonth.setMonth(newFirstDayOfMonth.getMonth()-1);

    // Replace html
    var lastCalendarHtml = getCalendarHtml(newFirstDayOfMonth.getMonth(),
                                            newFirstDayOfMonth.getFullYear());
    console.log("calendarHtml = " + lastCalendarHtml);
    document.getElementById("availabilityCalendar").innerHTML = lastCalendarHtml;
    document.getElementById("availabilityCalendar").setAttribute("month", newFirstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendar").setAttribute("year", newFirstDayOfMonth.getFullYear());
}

function showNextMonth() {
    // Get current month and increment
    var currentMonth = document.getElementById("availabilityCalendar").getAttribute("month");
    var currentYear = document.getElementById("availabilityCalendar").getAttribute("year");
    var newFirstDayOfMonth = new Date(currentYear, currentMonth, 1);
    newFirstDayOfMonth.setMonth(newFirstDayOfMonth.getMonth()+1);

    // Get availability data
    //$.get("http://localhost:5000/bookings/", function(data, status){
    //    console.log("Got bookings (" + status +"): " + data);
    //});
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log("Got bookings: " + this.responseText);
        }
    };
    xhttp.open("GET", "https://trefechanwen.herokuapp.com/bookings", true);
    xhttp.send();

    // Replace html
    var nextCalendarHtml = getCalendarHtml(newFirstDayOfMonth.getMonth(),
                                            newFirstDayOfMonth.getFullYear());
    console.log("calendarHtml = " + nextCalendarHtml);
    document.getElementById("availabilityCalendar").innerHTML = nextCalendarHtml;
    document.getElementById("availabilityCalendar").setAttribute("month", newFirstDayOfMonth.getMonth());
    document.getElementById("availabilityCalendar").setAttribute("year", newFirstDayOfMonth.getFullYear());
}


// Find current and next month
var firstDayOfMonth = new Date();
firstDayOfMonth.setDate(1);

var calendarHtml = getCalendarHtml(firstDayOfMonth.getMonth(), firstDayOfMonth.getFullYear());
console.log("calendarHtml = " + calendarHtml);

document.getElementById("lastMonth").onclick = showPreviousMonth;
document.getElementById("nextMonth").onclick = showNextMonth;
document.getElementById("availabilityCalendar").innerHTML = calendarHtml;
document.getElementById("availabilityCalendar").setAttribute("month", firstDayOfMonth.getMonth());
document.getElementById("availabilityCalendar").setAttribute("year", firstDayOfMonth.getFullYear());