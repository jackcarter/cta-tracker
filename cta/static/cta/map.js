"use strict";
var map;
var markers = [];
var listenerHandles = [];
var stopTypeIndicator = 'S';
var stopInfo = new google.maps.InfoWindow();

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
		if (points[i].type === stopTypeIndicator) {
			addStop(data.route_id, data.direction, points[i])
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

function getStopInfoContent(stop_id, stop_name) {
	var stop_id = stop_id;
	var stop_name = stop_name;
	var divId = 'wrapper-' + stop_id;
	var content = $('<div/>', {
		id: divId,
	});
	content.append(stop_name + '<br/>');
	return content;
}

function openStopInfo(predictions) {
	var prediction;
	var stop_id = predictions[0].stop_id;
	var stop_name = predictions[0].stop_name;
	var marker=markers[stop_id];
	var content = getStopInfoContent(stop_id, stop_name);
	for (var i=0; i<predictions.length; i++) {
		content.append($('<div/>', {
			text: predictions[i].route_direction + ': ' + predictions[i].predicted_time,
		}))	
	}
	stopInfo.close();
	stopInfo = new google.maps.InfoWindow({
		content: content[0], 
	  });
	stopInfo.open(map, marker);
}

function getPredictions(stop_id) {
	Dajaxice.cta.get_predictions(openStopInfo, {'stop_ids':[stop_id]});
}

function addStop(route_id, direction, stop) {
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
	markers[stop.stop_id]=marker;
	listenerHandles[stop.stop_id] = google.maps.event.addListener(marker, 'click', function() {
		getPredictions(stop.stop_id);
	});
}

function addStops(routeStops) {
	for (var i=0; i<routeStops.stops.length; i++) {
		addStop(routeStops.route_id, routeStops.direction, routeStops.stops[i]);
	}
}

function getStops(){
	var directions = [
		'Eastbound',
		'Westbound',
		'Northbound',
		'Southbound',
	]
	for (var i=0; i<directions.length;i++) {
		Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val(), 'direction':directions[i]});
	}
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