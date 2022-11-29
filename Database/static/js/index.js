/*Preloader*/
$(window).on('load', function () {
    setTimeout(function () {
        $('body').addClass('loaded');
    }, 700);
});

// Google Maps
var companyLocation = new google.maps.LatLng(-33.91866570922499, 151.23089819618647);
function initialize() {
    var mapProp = {
        center: companyLocation,
        zoom: 19,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("map"), mapProp);

    var marker = new google.maps.Marker({
        position: companyLocation,
    });

    marker.setMap(map);
}
google.maps.event.addDomListener(window, 'load', initialize);