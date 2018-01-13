function initMap() {
    var location = {lat: 52.009921, lng: -5.009119};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 9,
        center: location
    });
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}