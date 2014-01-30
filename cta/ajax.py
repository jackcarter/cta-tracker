from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import ctatracker
from models import Route, Stop

a = ctatracker.BusTracker()

def get_routes_from_cache():
	return [route.as_dict_no_stops() for route in Route.objects.all()]

def get_stops_from_cache(route, direction):
	stops = Stop.objects.filter(stoptoroute__route_id=route, stoptoroute__direction__direction=direction)
	return [stop.as_dict() for stop in stops]
	
def get_stops_helper(route):
	return_list = []
	directions = a.get_directions(route)
	for direction in directions:
		return_list.append(a.get_stops(route, direction))
	return return_list

@dajaxice_register
def get_stops(request, route):
	return simplejson.dumps(get_stops_helper(route))
#    return simplejson.dumps(get_stops_from_cache(route, direction))

@dajaxice_register
def get_patterns(request, route):
	return simplejson.dumps(a.get_patterns(route))
#    return simplejson.dumps(a.get_patterns(route))

@dajaxice_register
def get_routes(request):
	return simplejson.dumps(a.get_routes())
#    return simplejson.dumps(get_routes_from_cache())

@dajaxice_register
def get_predictions(request, stop_ids=None, route_ids=None, vehicle_ids=None, top=None):
	return simplejson.dumps(a.get_predictions(stop_ids, route_ids, vehicle_ids, top))

