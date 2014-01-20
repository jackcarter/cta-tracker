var map;
function initialize(){
	//Init google map:
	var mapDiv = document.getElementById('map_canvas');
	map = new google.maps.Map(mapDiv, {
		center: new google.maps.LatLng(41.910277822061, -87.686948776245),
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});
	
	//Populate routes dropdown:
	Dajaxice.cta.get_routes(getRoutesCallback);
}

function addRoutes(routes) {
	for (var route in routes) {
	    addRoute(routes[route].route_id, routes[route].route_name);
	  }
}

function addRoute(routeId, routeName) {
	$('#route-selector').append($("<option/>", {
	        value: routeId,
	        text: routeId + ' - ' + routeName
	    }));
}
function get_random_color() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

function addPattern(data) {
	var path = [];
	for (var point in data) {
		var latLng = new google.maps.LatLng(data[point].latitude, data[point].longitude);
		path.push(latLng);
	}
	console.log(path);
	var line = new google.maps.Polyline({
	    path: path,
	    strokeColor: get_random_color(),
	    strokeOpacity: 1.0,
	    strokeWeight: 2
	  });

	  line.setMap(map);
}

function addStops(routeStops) {
	for (var stop in routeStops) {
		var latLng = new google.maps.LatLng(routeStops[stop].latitude, routeStops[stop].longitude);
   		addStop(latLng);
	}
}

function addStop(latLng) {
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
}
