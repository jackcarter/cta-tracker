import ctatracker

a = ctatracker.BusTracker()
'''
print a.get_time()
print a.get_vehicles(vehicle_ids=['1567'])
print a.get_routes()



print a.get_stops('72','Eastbound')
print a.get_directions('49')

print a.get_predictions(['17404'], top=1)
'''
from cta.models import *
def save_routes():
	routes = a.get_routes()
	for route in routes[:1]:
		route_obj = Route(route_id=route['route'], route_name=route['route_name'])
		route_obj.save()
		directions = a.get_directions(route['route'])
		for direction in directions:
			direction_obj = Direction(direction=direction)
			stops = a.get_stops(route['route'], direction)
			for stop in stops:
				stop_obj = Stop(
					stop_id=stop['stop_id'],
					stop_name=stop['stop_name'],
					latitude=stop['latitude'],
					longitude=stop['longitude'],
				)
				stop_obj.save()
				route_obj.stops.add(stop_obj)
			direction_obj.save()
			route_obj.directions.add(direction_obj)
save_routes()