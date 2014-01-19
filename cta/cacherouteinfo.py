import ctatracker
from cta.models import Route, Stop, Direction, Vehicle, DirectionToRoute, StopToRoute

a = ctatracker.BusTracker()

def save_routes():
	routes = a.get_routes()
	for route in routes[:1]:
		route_obj = Route.objects.get_or_create(route_id=route['route'], route_name=route['route_name'])
		directions = a.get_directions(route['route'])
		for direction in directions:
			direction_obj = Direction.objects.get_or_create(direction=direction)
			stops = a.get_stops(route['route'], direction)
			for stop in stops:
				stop_obj = Stop.objects.get_or_create(
					route=route['route'],
					stop_id=stop['stop_id'],
					stop_name=stop['stop_name'],
					latitude=stop['latitude'],
					longitude=stop['longitude'],
				)
				stop_obj.save()
		
		r.stop_set.create()
		