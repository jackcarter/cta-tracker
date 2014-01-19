from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
import ctatracker

a = ctatracker.BusTracker()
@dajaxice_register
def sayhello(request):
    return simplejson.dumps(a.get_stops('72','Eastbound'))