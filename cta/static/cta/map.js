var map;
function initialize() {
	var mapDiv = document.getElementById('map_canvas');
	map = new google.maps.Map(mapDiv, {
		center: new google.maps.LatLng(41.910277822061, -87.686948776245),
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});
}

function addRoutes(data) {
	for (var route in data) {
	    addRoute(data[route].route, data[route].route_name);
	  }
}

function addRoute(routeId, routeName) {
	$('#route-selector').append($("<option/>", {
	        value: routeId,
	        text: routeId + ' - ' + routeName
	    }));
}

function addStops(data) {
  for (var stop in data) {
    addStop(data[stop].latitude, data[stop].longitude);
  }
}

function addStop(latitude, longitude) {
    var latLng = new google.maps.LatLng(latitude, longitude);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
}
