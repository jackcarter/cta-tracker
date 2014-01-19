import ctatracker
from cta.models import Route, Stop, Direction, Vehicle

a = ctatracker.BusTracker()

def save_routes():
	routes = a.get_routes()
	for route in routes[:10]:
		route_obj = Route(route_id=route['route'], route_name=route['route_name'])
		route_obj.save()
		directions = a.get_directions(route['route'])
		
		for direction in directions:
			direction_obj, direction_created = Direction.objects.get_or_create(direction=direction)

			if direction_created:	
				direction_obj.save()				
			route_obj.directions.add(direction_obj)
			
			stops = a.get_stops(route['route'], direction)

			for stop in stops:
				stop_obj, stop_created = Stop.objects.get_or_create(
					stop_id=stop['stop_id'],
					stop_name=stop['stop_name'],
					latitude=stop['latitude'],
					longitude=stop['longitude'],
				)
				if stop_created:
					stop_obj.save()
				route_obj.stops.add(stop_obj)	

#		route_obj.save()