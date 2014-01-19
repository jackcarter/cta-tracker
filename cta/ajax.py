from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import ctatracker
from models import Route, Stop, Direction, Vehicle

a = ctatracker.BusTracker()
@dajaxice_register
def get_stops(request, route, direction):
    return simplejson.dumps(a.get_stops(route, direction))

@dajaxice_register
def get_routes(request):
    return simplejson.dumps(a.get_routes())
