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

def get_directions_from_cache(route_id):
	route = route_col.find({'route_id':route_id},{'_id':0})
	
def get_stops_helper(route_id):
	return_list = []
	directions = get_directions_from_cache(route_id)
	for direction in directions:
		return_list.append(a.get_stops(route_id, direction))
	return return_list

@dajaxice_register
def get_stops(request, route_id):
	return simplejson.dumps(get_stops_helper(route_id))
#    return simplejson.dumps(get_stops_from_cache(route, direction))

@dajaxice_register
def get_pattern(request, route_id):
	return simplejson.dumps(a.get_pattern(route_id))

@dajaxice_register
def get_routes(request):
	return simplejson.dumps(get_routes_from_cache())

@dajaxice_register
def get_predictions(request, stop_ids=None, route_ids=None, vehicle_ids=None, top=None):
	return simplejson.dumps(a.get_predictions(stop_ids, route_ids, vehicle_ids, top))
	
@dajaxice_register
def get_vehicles(request, route_ids=None, vehicle_ids=None):
	return simplejson.dumps({'route_ids':route_ids, 'response':a.get_vehicles(route_ids, vehicle_ids)})

