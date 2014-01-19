from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import ctatracker

a = ctatracker.BusTracker()
@dajaxice_register
def getStops(request, route):
    return simplejson.dumps(a.get_stops(route,'Eastbound'))

@dajaxice_register
def getRoutes(request):
    return simplejson.dumps(a.get_routes())