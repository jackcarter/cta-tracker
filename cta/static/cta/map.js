"use strict";
var map;
var markers = [];
var stopInfos = [];

function addRoutes(routes) {
	var route;
	for (route in routes) {
		addRoute(routes[route].route_id, routes[route].route_name);
	  }
}

function addRoute(routeId, routeName) {
	$('#route-selector').append($("<option/>", {
			value: routeId,
			text: routeId + ' - ' + routeName
		}));
}

function getRoutes() {
	Dajaxice.cta.get_routes(addRoutes);
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
	var point;
	var latLng;
	var points = data['point']
	var i;

	for (var i=0; i<points.length; i++) {
		console.log(points[i]);
		if (points[i].type === 'S') {
			addStop(points[i])
		}
		latLng = new google.maps.LatLng(points[i].latitude, points[i].longitude);
		path.push(latLng);
	}

	var line = new google.maps.Polyline({
		path: path,
		strokeColor: get_random_color(),
		strokeOpacity: 0.5,
		strokeWeight: 4
	  });

	  line.setMap(map);
}

function addPatterns(patterns) {
	var pattern;
	for (pattern in patterns) {
		addPattern(patterns[pattern]);
	}
}

function getPatterns() {
	Dajaxice.cta.get_patterns(addPatterns, {'route':$('#route-selector').val()});
}

function addPredictions(predictions) {
	var prediction;
	console.log(predictions);
	for (prediction in predictions) {
		//console.log(prediction);
	}
}

function getPredictions(stop_id) {
	Dajaxice.cta.get_predictions(addPredictions, {'stop_ids':[stop_id]});
}

function addStop(stop) {
	var latLng = new google.maps.LatLng(stop.latitude, stop.longitude);
	var marker = new google.maps.Marker({
	  position: latLng,
	  map: map,
	  icon: {
		path: google.maps.SymbolPath.CIRCLE,
		scale: 3,
		strokeColor: 'black',
	  },
	});
	var infoWindow = new google.maps.InfoWindow({
		content: $('<button/>', {
			text: stop.stop_name,
			id: stop.stop_id,
			click: function(){getPredictions(stop.stop_id)},
		})[0]
	  });
	google.maps.event.addListener(marker, 'click', function() {
		infoWindow.open(map, this);
	});
	google.maps.event.addListener(map, 'click', function() {
		for(var i=0; i<stopInfos.length; i++) {
			stopInfos[i].close();
		}
	});
	markers.push(marker);
	stopInfos.push(infoWindow);
}

function addStops(routeStops) {
	var i;
	for (var i=0; i<routeStops.length; i++) {
		addStop(routeStops[i]);
	}
}

function getStops(){
	Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val(), 'direction':'Eastbound'});
	Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val(), 'direction':'Westbound'});
	Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val(), 'direction':'Northbound'});
	Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val(), 'direction':'Southbound'});
}

function initialize() {
	//Init google map:
	var mapDiv = document.getElementById('map_canvas');
	map = new google.maps.Map(mapDiv, {
		center: new google.maps.LatLng(41.910277822061, -87.686948776245),
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});
	
	//Populate routes dropdown:
	getRoutes();
}