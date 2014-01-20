from cta.models import Route, Direction, Stop, StopToRoute

def get_routes():
	routes = {route.as_dict() for route in Route.objects.all()}