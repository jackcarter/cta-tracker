from django.db import models
from django.utils import timezone
from mongoengine import *


class Stop(EmbeddedDocument):
	stop_id = IntegerField(required = True)
	stop_name = CharField(max_length = 100)
	latitude = FloatField()
	longitude = FloatField()

	def __unicode__(self):
		return self.stop_name


class Route(Document):
	route_id = CharField(max_length = 8, required=True)
	route_name = CharField(max_length = 100)
	directions = ListField()
	stops = ListField(EmbeddedDocumentField(Stop))
	
	def __unicode__(self):
		return self.route_name