from django.contrib import admin
from models import Route, Stop, Direction, Vehicle, StopToRoute


class StopToRouteInline(admin.StackedInline):
	model = StopToRoute
	

class RouteAdmin(admin.ModelAdmin):
	inlines = [StopToRouteInline]

admin.site.register(Route, RouteAdmin)
admin.site.register(Stop)
admin.site.register(Direction)
admin.site.register(Vehicle)