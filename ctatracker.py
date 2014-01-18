import requests
import keys
from datetime import datetime
import xml.etree.ElementTree as ET


class BusTracker(object):
	def __init__(self):
		self.base_url = 'http://www.ctabustracker.com/bustime/api/v1/'

	def parse_time(self, xml_timestamp):
		return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M')
	def parse_time_seconds(self, xml_timestamp):
		return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M:%S')
	def parse_double(self, xml_double):
		return float(xml_double) if xml_double is not None else None
	def parse_int(self, xml_int):
		return int(xml_int) if xml_int is not None else None

	def run_query(self, request_string, params):
		r = requests.get(self.base_url + request_string, params=params)
		r.encoding = 'utf-8'
		root = ET.fromstring(r.text)
		return root
	
	def get_time(self):
			params = {
				'key':keys.cta,
			}
			request_string = 'gettime'
			root = self.run_query(request_string, params)
			d = self.parse_time_seconds(root.find('tm').text)
			return d

	def get_vehicles(self, vehicle_ids=None, route_ids=None):
		params = {
			'key':keys.cta,
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
				'route'				:	v.find('rt').text,
				'destination'		:	v.find('des').text,
				'pattern_distance'	:	self.parse_int(v.find('pdist').text),
				'delayed'			:	True if v.find('dly') is not None else False,
			}
		for v in root.findall('vehicle'):
			vehicles.append(parse_vehicle(v))
		return vehicles

	def get_routes(self):
		params = {
			'key':keys.cta,
		}
		request_string = 'getroutes'
		root = self.run_query(request_string, params)
		routes = []
		def parse_route(r):
			return {
				'route'		:	r.find('rt').text,
				'route_name':	r.find('rtnm').text,
			}
		for r in root.findall('route'):
			routes.append(parse_route(r))
		return routes

	def get_directions(self, route):
		params = {
			'key':keys.cta,
			'rt':route,
		}
		request_string = 'getdirections'
		root = self.run_query(request_string, params)
		directions = []
		for d in root.findall('dir'):
			directions.append(d.text)
		return directions
	
	def get_stops(self, route, direction):
		params = {
			'key'	:	keys.cta,
			'rt'	:	route,
			'dir'	:	direction,
		}
		request_string = 'getstops'
		root = self.run_query(request_string, params)
		stops = []
		def parse_stop(v):
			return {
				'stop_id'	:	s.find('stpid').text,
				'stop_name'	:	s.find('stpnm').text,
				'latitude'	:	self.parse_double(s.find('lat').text),
				'longitude'	:	self.parse_double(s.find('lon').text),
			}
		for s in root.findall('stop'):
			stops.append(parse_stop(s))
		return stops

	def get_predictions(self, stop_ids=None, route_ids=None, vehicle_ids=None, top=None):
		params = {
			'key'	:	keys.cta,
			'vid'	:	','.join(vehicle_ids) if vehicle_ids else None,
			'rt'	:	','.join(route_ids) if route_ids else None,
			'stpid'	:	','.join(stop_ids) if stop_ids else None,
			'top'	:	top
		}
		request_string = 'getpredictions'
		root = self.run_query(request_string, params)
		predictions = []
		def parse_prediction(p):
			return {
				'timestamp'			:	self.parse_time(p.find('tmstmp').text),
				'type'				:	p.find('typ').text,
				'stop_id'			:	p.find('stpid').text,
				'stop_name'			:	p.find('stpnm').text,
				'vehicle_id'		:	p.find('vid').text,
				'distance_to_stop'	:	self.parse_int(p.find('dstp').text),
				'route'				:	p.find('rt').text,
				'route_direction'	:	p.find('rtdir').text,
				'destination'		:	p.find('des').text,
				'predicted_time'	:	self.parse_time(p.find('prdtm').text),
				'delayed'			:	True if p.find('dly') is not None else False,
			}
		for p in root.findall('prd'):
			predictions.append(parse_prediction(p))
		return predictions