/*jslint browser: true*/
/*jslint plusplus: true*/
/*global $, jQuery, alert, google, Dajaxice*/
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

function sortByRouteId(objects) {
	return objects.sort(function(a, b) {
		return a.route_id - b.route_id;
	});
}

function getStopInfoContent(stop_id, stop_name) {
	var div_id = getDivId(stop_id)
		, content = $('<div/>', {
			id: div_id
		});
	content.append(stop_name + '<br/>');
	content.addClass('infoWindow');
	return content;
}

function openStopInfo(predictions) {
	predictions = sortByRouteId(predictions);
	var stop_id = predictions[0].stop_id
		, stop_name = predictions[0].stop_name
		, marker=markers[stop_id]
		, content = getStopInfoContent(stop_id, stop_name)
		, predicted_time
		, timestamp
		, time_until
		, route_id
		, i;

	for (i=0; i<predictions.length; i++) {
		predicted_time = new Date(predictions[i].predicted_time);
		timestamp = new Date(predictions[i].timestamp);
		time_until = (predicted_time - timestamp)/(1000*60);
		route_id = predictions[i].route_id;
		content.append($('<div/>', {
			text: route_id + ' ' + predictions[i].route_direction + ': ' + time_until + 'm'
		}))
	}
	stopInfo.close();
	stopInfo.setContent(content[0]);
	stopInfo.open(map, marker);
	window.setTimeout(function(){addUpdateButton(stop_id);}, 1000*60);
}

function getPredictions(stop_id) {
	Dajaxice.cta.get_predictions(openStopInfo, {'stop_ids':[stop_id]});
}

function addUpdateButton(stop_id) {
	var div_id = getDivId(stop_id)
		, buttonId = 'button-' + stop_id;
	$('#'+div_id).append($('<button/>', {
		text: 'Update predictions'
		, id: buttonId
		, click: function(){getPredictions(stop_id);}
	}));
	refreshStopInfo(stop_id);
}

function addRoute(routeId, routeName) {
	$('#route-selector').append($("<option/>", {
			value: routeId
			, text: routeId + ' - ' + routeName
		}));
}

function addRoutes(routes) {
	var route;
	for (route in routes) {
		if (routes.hasOwnProperty(route)) {
			//Skip prototype chain
			addRoute(routes[route].route_id, routes[route].route_name);
		}
	}
}

function getRoutes() {
	Dajaxice.cta.get_routes(addRoutes);
}

function get_random_color() {
	var letters = '0123456789ABCDEF'.split('')
		, color = '#'
		, i;
	for (i = 0; i < 6; i++ ) {
		color += letters[Math.round(Math.random() * 15)];
	}
	return color;
}

function addStop(stop) {
	var latLng = new google.maps.LatLng(stop.latitude, stop.longitude)
		, marker = new google.maps.Marker({
	  position: latLng,
	  map: map,
	  icon: {
		path: google.maps.SymbolPath.CIRCLE
		, scale: 3
		, strokeColor: 'black'
	  }
	});
	markers[stop.stop_id]=marker;
	listenerHandles[stop.stop_id] = google.maps.event.addListener(marker, 'click', function() {
		getPredictions(stop.stop_id);
	});
}
var asdf;
function addStops(routeStops) {
	var i, j;
	asdf = routeStops;
	for (j=0; j<routeStops.length; j++) {
		for (i=0; i<routeStops[j].stops.length; i++) {
			addStop(routeStops[j].stops[i]);
		}	
	}
}

function getStops(){
	Dajaxice.cta.get_stops(addStops, {'route_id':$('#route-selector').val()});
}

function addPattern(data) {
	var path = []
		, latLng
		, points = data.point
		, i
		, line = new google.maps.Polyline({
			path: path,
			strokeColor: get_random_color(),
			strokeOpacity: 0.5,
			strokeWeight: 4
	  	});

	for (i=0; i<points.length; i++) {
		if (points[i].type === stopTypeIndicator) {
			addStop(points[i]);
		}
		latLng = new google.maps.LatLng(points[i].latitude, points[i].longitude);
		path.push(latLng);
	}
	
	line.setMap(map);
}

function addPatterns(patterns) {
	var pattern;
	for (pattern in patterns) {
		if (patterns.hasOwnProperty(pattern)) {
			//Skip prototype chain
			addPattern(patterns[pattern]);
		}
	}
}

function getPatterns() {
	Dajaxice.cta.get_pattern(addPatterns, {'route_id':$('#route-selector').val()});
}

function getBusIcon(heading) {
	return {
		path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
		, scale: 3
		, strokeColor: 'red'
		, rotation: heading
	  };
}

function addVehicle(vehicle) {
	var latLng = new google.maps.LatLng(vehicle.latitude, vehicle.longitude)
		, marker = new google.maps.Marker({
			position: latLng,
			map: map,
			icon: getBusIcon(vehicle.heading),
		})
		, vehicle_marker = vehicle;

	vehicle_marker.marker = marker;
	vehicles[vehicle.route_id][vehicle.vehicle_id]=vehicle_marker;
}

function updateVehicle(newVehicle, oldVehicle) {
	var fromLat = oldVehicle.latitude
	, fromLng = oldVehicle.longitude
	, toLat = newVehicle.latitude
	, toLng = newVehicle.longitude
	, fromHead = oldVehicle.heading
	, toHead = newVehicle.heading
	, marker = oldVehicle.marker
	, intermediateLatLngs = []
	, intermediateHeadings = []
	, curLat
	, curLng
	, curHead
	, degrees = toHead - fromHead
	, i;
	
	oldVehicle = newVehicle;
	oldVehicle.marker = marker;
	
	if (degrees>180) {
		degrees -= 360;
	} else if (degrees<-180) {
		degrees += 360;
	}
	for (i=0; i<1; i+=0.01) {
		curLat = fromLat + i*(toLat-fromLat);
		curLng = fromLng + i*(toLng-fromLng);
		curHead = fromHead + i*(degrees);
		intermediateLatLngs.push(new google.maps.LatLng(curLat, curLng));
		intermediateHeadings.push(curHead);
	}
	function animate(marker, intermediateLatLngs, intermediateHeadings) {
		marker.setPosition(intermediateLatLngs[0]);
		marker.setIcon(getBusIcon(intermediateHeadings[0]));
		var newIntermediateLatLngs = intermediateLatLngs.slice(1);
		var newIntermediateHeadings = intermediateHeadings.slice(1);
		if (newIntermediateLatLngs.length > 0) {
			setTimeout(function() {
				animate(marker, newIntermediateLatLngs, newIntermediateHeadings)
			}, 10);
		}
	}
//	console.log(oldVehicle, newVehicle);
	animate(oldVehicle.marker, intermediateLatLngs, intermediateHeadings);
	return oldVehicle;
}

function addOrUpdateVehicle(newVehicle) {
	var route_id = newVehicle.route_id
	, vehicleFound = false
	, oldVehicleId;
	
	for (oldVehicleId in vehicles[route_id]) {
		if (vehicles[route_id].hasOwnProperty(oldVehicleId)) {
			//Skip prototype chain
			//Update old vehicle if we already have this vehicle_id on this route
			if (oldVehicleId === newVehicle.vehicle_id) {
				vehicles[route_id][oldVehicleId] = updateVehicle(newVehicle, vehicles[route_id][oldVehicleId]);
				vehicleFound = true;
			}
			
		}
	}
	//If this vehicle ID wasn't on the route last time we updated, we won't have found it
	//So, let's add it as a new one
	if (!vehicleFound) {
		addVehicle(newVehicle);
	}
}

function updateVehicles(newVehicles) {
	var i;
	
	for (i=0;i<newVehicles.length;i++) {
		addOrUpdateVehicle(newVehicles[i]);
	}
}

//TODO: Finish this
function removeMissingVehicles(newVehicles, routeId) {
	var oldIds = []
	, newIds = []
	, i;
	for (i=0;i<vehicles[routeId].length;i++) {
		oldIds.push(vehicles[routeId][i].vehicle_id);
	}
	for (i=0;i<newVehicles.length;i++) {
		oldIds.push(newVehicles[i].vehicle_id);
	}
	vehicles[routeId] = $(vehicles[routeId]).not(newVehicles).get();
}

var asdf;
function addVehicles(new_vehicles) {
	asdf = new_vehicles.response;
	var route_id = new_vehicles.route_ids[0]; //TODO: generalize to multiple route_ids
	if (typeof vehicles[route_id] === 'undefined') {
		//this will break if I try to call getVehicles for 2 routes; one loaded and one not
		vehicles[route_id] = {};
	}
	updateVehicles(new_vehicles.response, route_id);
}

function getVehicles(){
	var route_id = $('#route-selector').val();
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