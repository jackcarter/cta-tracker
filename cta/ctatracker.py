import os
import requests
from datetime import datetime
import xml.etree.ElementTree as ET


class BusTracker(object):
	def __init__(self):
		self.base_url = 'http://www.ctabustracker.com/bustime/api/v1/'
		self.cta_api_key = os.environ.get('CTA_API_KEY')

	def parse_time(self, xml_timestamp):
		return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M')
	def parse_time_RfC_3339(self, xml_timestamp):
		return self.parse_time(xml_timestamp).strftime('%Y-%m-%dT%H:%M:%S')
	def parse_time_seconds(self, xml_timestamp):
		return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M:%S')
	def parse_double(self, xml_double):
		return float(xml_double) if xml_double is not None else None
	def parse_int(self, xml_int):
		return int(float(xml_int)) if xml_int is not None else None

	def run_query(self, request_string, params):
		r = requests.get(self.base_url + request_string, params=params)
		r.encoding = 'utf-8'
		root = ET.fromstring(r.text)
		return root
	
	def get_time(self):
			params = {
				'key':self.cta_api_key,
			}
			request_string = 'gettime'
			root = self.run_query(request_string, params)
			d = self.parse_time_seconds(root.find('tm').text)
			return d

	def get_vehicles(self, vehicle_ids=None, route_ids=None):
		params = {
			'key':self.cta_api_key,
			'vid':','.join(vehicle_ids) if vehicle_ids else None,
			'rt':','.join(route_ids) if route_ids else None,
		}
		request_string = 'getvehicles'
		root = self.run_query(request_string, params)
		vehicles = []
		def parse_vehicle(v):
			return {
				'vehicle_id'		:	v.find('vid').text,
				'timestamp'			:	self.parse_time(v.find('tmstmp').text),
				'latitude'			:	self.parse_double(v.find('lat').text),
				'longitude'			:	self.parse_double(v.find('lon').text),
				'heading'			:	self.parse_int(v.find('hdg').text),
				'pattern_id'		:	v.find('pid').text,
				'route_id'				:	v.find('rt').text,
				'destination'		:	v.find('des').text,
				'pattern_distance'	:	self.parse_int(v.find('pdist').text),
				'delayed'			:	True if v.find('dly') is not None else False,
			}
		for v in root.findall('vehicle'):
			vehicles.append(parse_vehicle(v))
		return vehicles

	def get_directions(self, route_id):
		params = {
			'key':self.cta_api_key,
			'rt':route_id,
		}
		request_string = 'getdirections'
		root = self.run_query(request_string, params)
		directions = []
		for d in root.findall('dir'):
			directions.append(d.text)
		return directions
			
	def get_routes(self):
		params = {
			'key':self.cta_api_key,
		}
		request_string = 'getroutes'
		root = self.run_query(request_string, params)
		routes = []
		def parse_route(r):
			return {
				'route_id'		:	r.find('rt').text,
				'route_name':	r.find('rtnm').text,
			}
		for r in root.findall('route'):
			routes.append(parse_route(r))
		return routes
	
	def get_stops(self, route_id, direction):
		params = {
			'key'	:	self.cta_api_key,
			'rt'	:	route_id,
			'dir'	:	direction,
		}
		request_string = 'getstops'
		root = self.run_query(request_string, params)
		stops = []
		def parse_stop(v):
			return {
				'stop_id'	:	self.parse_int(s.find('stpid').text),
				'stop_name'	:	s.find('stpnm').text,
				'latitude'	:	self.parse_double(s.find('lat').text),
				'longitude'	:	self.parse_double(s.find('lon').text),
			}
		for s in root.findall('stop'):
			stops.append(parse_stop(s))
		return {
			'route_id':route_id,
			'direction':direction,
			'stops':stops,
		}

	def get_patterns(self, route_id=None, pattern_ids=None):
		params = {
			'key'	:	self.cta_api_key,
			'pid'	:	','.join(pattern_ids) if pattern_ids else None,
			'rt'	:	route_id if route_id else None,
		}
		request_string = 'getpatterns'
		root = self.run_query(request_string, params)
		patterns = []
		def parse_point(point):
			if point.find('typ').text == 'S': #S means it's a stop
				return {
					'sequence'			:	self.parse_int(point.find('seq').text),
					'type'				:	point.find('typ').text,
					'stop_id'			:	self.parse_int(point.find('stpid').text),
					'stop_name'			:	point.find('stpnm').text,
					'point_distance'	:	self.parse_double(point.find('pdist').text),
					'latitude'			:	self.parse_double(point.find('lat').text),
					'longitude'			:	self.parse_double(point.find('lon').text),
				}
			else: #It's a waypoint (type='W'; there's no stpid/stpnm/pdist)
				return {
					'sequence'			:	self.parse_int(point.find('seq').text),
					'type'				:	point.find('typ').text,
					'latitude'			:	self.parse_double(point.find('lat').text),
					'longitude'			:	self.parse_double(point.find('lon').text),
				}
		def parse_pattern(pattern):
			return {
				'route_id'			:	route_id,
				'pattern_id'		:	self.parse_int(pattern.find('pid').text),
				'length'			:	self.parse_int(pattern.find('ln').text),
				'direction'			:	pattern.find('rtdir').text,
				'point'				:	[parse_point(point) for point in pattern.findall('pt')],
			}
		for pattern in root.findall('ptr'):
			patterns.append(parse_pattern(pattern))
		return patterns

	def get_predictions(self, stop_ids=None, route_ids=None, vehicle_ids=None, top=None):
		params = {
			'key'	:	self.cta_api_key,
			'vid'	:	','.join(vehicle_ids) if vehicle_ids else None,
			'rt'	:	','.join(route_ids) if route_ids else None,
			'stpid'	:	','.join([str(id) for id in stop_ids]) if stop_ids else None,
			'top'	:	top
		}
		request_string = 'getpredictions'
		root = self.run_query(request_string, params)
		predictions = []
		def parse_prediction(p):
			return {
				'timestamp'			:	self.parse_time_RfC_3339(p.find('tmstmp').text),
				'type'				:	p.find('typ').text,
				'stop_id'			:	self.parse_int(p.find('stpid').text),
				'stop_name'			:	p.find('stpnm').text,
				'vehicle_id'		:	p.find('vid').text,
				'distance_to_stop'	:	self.parse_int(p.find('dstp').text),
				'route_id'			:	p.find('rt').text,
				'route_direction'	:	p.find('rtdir').text,
				'destination'		:	p.find('des').text,
				'predicted_time'	:	self.parse_time_RfC_3339(p.find('prdtm').text),
				'delayed'			:	True if p.find('dly') is not None else False,
			}
		for p in root.findall('prd'):
			predictions.append(parse_prediction(p))
		return predictions