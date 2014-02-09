"use strict";
var map;
var markers = [];
var listenerHandles = [];
var stopTypeIndicator = 'S';
var stopInfo = new google.maps.InfoWindow();
var vehicles = {};

function refreshStopInfo(stop_id) {
	stopInfo.close();
	stopInfo.open(map, markers[stop_id]);
}

function getDivId(stop_id) {
	return 'wrapper-' + stop_id;
}

function addUpdateButton(stop_id) {
	var div_id = getDivId(stop_id);
	var buttonId = 'button-' + stop_id;
	$('#'+div_id).append($('<button/>', {
		text: 'Update predictions',
		id: buttonId,
		click: function(){getPredictions(stop_id)},
	}));
	refreshStopInfo(stop_id);
}

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
	Dajaxice.cta.get_pattern(addPatterns, {'route':$('#route-selector').val()});
}

function getStopInfoContent(stop_id, stop_name) {
	var stop_id = stop_id;
	var stop_name = stop_name;
	var div_id = getDivId(stop_id);
	var content = $('<div/>', {
		id: div_id,
	});
	content.append(stop_name + '<br/>');
	content.addClass('infoWindow');
	return content;
}

function sortByRouteId(objects) {
	return objects.sort(function(a, b) {
		return a.route_id - b.route_id
	})
}

function openStopInfo(predictions) {
	predictions = sortByRouteId(predictions);
	var prediction;
	var stop_id = predictions[0].stop_id;
	var stop_name = predictions[0].stop_name;
	var marker=markers[stop_id];
	var content = getStopInfoContent(stop_id, stop_name);
	var predicted_time;
	var timestamp;
	var time_until;
	var route_id;
	for (var i=0; i<predictions.length; i++) {
		predicted_time = new Date(predictions[i].predicted_time);
		timestamp = new Date(predictions[i].timestamp);
		time_until = (predicted_time - timestamp)/(1000*60);
		route_id = predictions[i].route_id;
		content.append($('<div/>', {
			text: route_id + ' ' + predictions[i].route_direction + ': ' + time_until + 'm',
		}))	
	}
	stopInfo.close();
	stopInfo.setContent(content[0]);
	stopInfo.open(map, marker);
	window.setTimeout(function(){addUpdateButton(stop_id)}, 1000*60);
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
	for (var j=0; j<routeStops.length; j++) {
		for (var i=0; i<routeStops[j].stops.length; i++) {
			addStop(routeStops[j].route_id, routeStops[j].direction, routeStops[j].stops[i]);
		}	
	}
}

function getStops(){
	Dajaxice.cta.get_stops(addStops, {'route':$('#route-selector').val()});
}

function addVehicle(vehicle) {
	var latLng = new google.maps.LatLng(vehicle.latitude, vehicle.longitude);
	var marker = new google.maps.Marker({
	  position: latLng,
	  map: map,
	  icon: {
		path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
		scale: 3,
		strokeColor: 'red',
		rotation: vehicle.heading,
	  },
	});
	var vehicle_marker = vehicle;
	vehicle_marker['marker'] = marker;
	vehicles[vehicle.route_id].push(vehicle_marker);
}

function addVehicles(new_vehicles) {
	console.log(new_vehicles);
	for (var i=0;i<new_vehicles.length;i++) {
		addVehicle(new_vehicles[i]);
	}
}

function getVehicles(){
	var route_id = $('#route-selector').val();
	if (typeof vehicles[route_id] !== 'undefined') {
		for (var i=0;i<vehicles[route_id].length;i++) {
			vehicles[route_id][i]['marker'].setMap(null);
		}
	}
	vehicles[route_id] = [];
	Dajaxice.cta.get_vehicles(addVehicles, {'route_ids':[route_id]})
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