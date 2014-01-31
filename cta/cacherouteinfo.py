import cta.ctatracker
from cta.models import Route, Stop
import pymongo
import os
mongo = os.environ.get('MONGOHQ_URL')
connection = pymongo.Connection(mongo)
db = connection.get_default_database()

a = cta.ctatracker.BusTracker()

def build_stop(stops_by_direction):
	stop = Stop(
		stop_id=stops_by_direction['stop_id'],
		stop_name=stops_by_direction['stop_name'],
		latitude=stops_by_direction['latitude'],
		longitude=stops_by_direction['longitude'],
		direction=stops_by_direction['direction'],
	)
	return stop

def save_routes():
	routes = a.get_routes()
	for route in routes:
		route['directions'] = a.get_directions(route['route_id'])
	route_col = db.routes
	route_col.insert(routes)