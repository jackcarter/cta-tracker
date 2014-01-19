from django.db import models
from django.utils import timezone


class Direction(models.Model):
	direction = models.CharField(max_length = 40, null=True)
	

class Route(models.Model):
	route_id = models.CharField(max_length = 8)
	route_name = models.CharField(max_length = 100)
	directions = models.ManyToManyField(Direction, blank=True, null=True, through='DirectionToRoute')
	stops = models.ManyToManyField(Stop, blank=True, null=True, through='StopToRoute')

	def __unicode__(self):
		return self.route_name


class Stop(models.Model):
	route = models.ForeignKey(Route)
	stop_id = models.CharField(max_length = 8)
	stop_name = models.CharField(max_length = 100)
	latitude = models.FloatField()
	longitude = models.FloatField()

	def __unicode__(self):
		return self.stop_name


class Vehicle(models.Model):
	pass
	

class DirectionToRoute(models.Model):
	route = models.ForeignKey(Route)
	direction = models.ForeignKey(Direction)
	
	class Meta:
		verbose_name = "Direction"


class StopToRoute(models.Model):
	route = models.ForeignKey(Route)
	stop = models.ForeignKey(Stop)

	class Meta:
		verbose_name = "Stop"