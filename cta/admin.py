from django.contrib import admin
from models import Route, Stop, Direction, Vehicle, DirectionToRoute, StopToRoute

# Register your models here.

class DirectionToRouteInline(admin.TabularInline):
    model = DirectionToRoute


class StopToRouteInline(admin.TabularInline):
    model = StopToRoute


class RouteAdmin(admin.ModelAdmin):
    #inlines = [CommentInline, CategoryToPostInline]
    inlines = [DirectionToRouteInline, StopToRouteInline]

admin.site.register(Route, RouteAdmin)
admin.site.register(Stop)
admin.site.register(Direction)
admin.site.register(Vehicle)