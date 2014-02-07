from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import cta.ctatracker
from cta.models import Route, Stop

import pymongo
import os
mongo = os.environ.get('MONGOHQ_URL')
connection = pymongo.Connection(mongo)
db = connection.jackdb
route_col = db.routes

a = cta.ctatracker.BusTracker()

def get_routes_from_cache():
	routes = []
	for route in route_col.find({},{'_id':0}):
		routes.append(route)
	return routes

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
def get_pattern(request, route):
	return simplejson.dumps(a.get_patterns(route))
#    return simplejson.dumps(a.get_patterns(route))

@dajaxice_register
def get_routes(request):
	r = simplejson.dumps(get_routes_from_cache())
	return r#'{a:"1"}'
	#return simplejson.dumps(a.get_routes())

@dajaxice_register
def get_predictions(request, stop_ids=None, route_ids=None, vehicle_ids=None, top=None):
	return simplejson.dumps(a.get_predictions(stop_ids, route_ids, vehicle_ids, top))
	
@dajaxice_register
def get_vehicles(request, route_ids=None, vehicle_ids=None):
	return simplejson.dumps(a.get_vehicles(route_ids, vehicle_ids))

