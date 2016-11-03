function initialize() {
     var options = {
     types: ['(cities)']
    };
    var input = document.getElementById('id_city');
    var country_code = "";
    var autocomplete = new google.maps.places.Autocomplete(input, options);
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var place = autocomplete.getPlace();
        for (var i = 0; i < place.address_components.length; i++) {
           var addressType = place.address_components[i].types[0];
           if (addressType == "country") {
               country_code = place.address_components[i].short_name;
             }
           }
        document.getElementById('lat').value = place.geometry.location.lat();
        document.getElementById('lon').value = place.geometry.location.lng();
    });
}
google.maps.event.addDomListener(window, 'load', initialize);