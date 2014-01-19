var map;
function initialize() {
	var mapDiv = document.getElementById('map_canvas');
	map = new google.maps.Map(mapDiv, {
		center: new google.maps.LatLng(41.910277822061, -87.686948776245),
		zoom: 12,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});
}
function addStops(data) {
  for (var object in data) {
    var latLng = new google.maps.LatLng(data[object].latitude, data[object].longitude);
	console.log(data[object]);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
  }
}
function addStop(latitude, longitude) {
    var latLng = new google.maps.LatLng(latitude, longitude);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
}
