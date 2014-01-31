import cta.ctatracker
from cta.models import Route, Stop

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
		directions = a.get_directions(route['route_id'])
		stops_by_direction = []
		stops = []
		'''
		for direction in directions:
			stops_by_direction = a.get_stops(route['route_id'], direction)
			for stop_by_direction in stops_by_direction:
				stop = Stop(
					stop_id=stops_by_direction['stop_id'],
					stop_name=stops_by_direction['stop_name'],
					latitude=stops_by_direction['latitude'],
					longitude=stops_by_direction['longitude'],
					direction=stops_by_direction['direction'],
				)		
		'''
		route_obj = Route(
			route_id=route['route_id'],
			route_name=route['route_name'],
			directions=directions,
#			stops=[build_stop(json_stop) for json_stop in stops_by_direction],
		)
		route_obj.save()