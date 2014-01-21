from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import ctatracker
from models import Route, Stop, Direction, Vehicle

a = ctatracker.BusTracker()

def get_routes_from_cache():
	return [route.as_dict_no_stops() for route in Route.objects.all()]

def get_stops_from_cache(route, direction):
	stops = Stop.objects.filter(stoptoroute__route_id=route, stoptoroute__direction__direction=direction)
	return [stop.as_dict() for stop in stops]

@dajaxice_register
def get_stops(request, route, direction):
    return simplejson.dumps(get_stops_from_cache(route, direction))

@dajaxice_register
def get_patterns(request, route):
    return simplejson.dumps(a.get_patterns(route))

@dajaxice_register
def get_routes(request):
    return simplejson.dumps(get_routes_from_cache())
