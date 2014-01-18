import requests
import keys
from datetime import datetime
import xml.etree.ElementTree as ET

base_url = "http://www.ctabustracker.com/bustime/api/v1/"
def parse_time(xml_timestamp):
	return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M')
def parse_time_seconds(xml_timestamp):
	return datetime.strptime(xml_timestamp, '%Y%m%d %H:%M:%S')
def parse_double(xml_double):
	return float(xml_double) if xml_double is not None else None
def parse_int(xml_int):
	return int(xml_int) if xml_int is not None else None
def get_time():
	params = {
		"key":keys.cta,
	}
	request_string = "gettime"
	r = requests.get(base_url + request_string, params=params)
	r.encoding = "utf-8"
	root = ET.fromstring(r.text)
	d = parse_time_seconds(root.find('tm').text)
	return d

def get_vehicles(vehicle_ids=None, route_ids=None):
	params = {
		"key":keys.cta,
		"vid":",".join(vehicle_ids) if vehicle_ids else None,
		"rt":",".join(route_ids) if route_ids else None,
	}
	request_string = "getvehicles"
	r = requests.get(base_url + request_string, params=params)
	r.encoding = "utf-8"
	root = ET.fromstring(r.text)
	vehicles = []
	def parse_vehicle(v):
		return {
			"vehicle_id"		:	v.find("vid").text,
			"timestamp"			:	parse_time(v.find("tmstmp").text),
			"latitude"			:	parse_double(v.find("lat").text),
			"longitude"			:	parse_double(v.find("lon").text),
			"heading"			:	parse_int(v.find("hdg").text),
			"pattern_id"		:	v.find("pid").text,
			"route"				:	v.find("rt").text,
			"destination"		:	v.find("des").text,
			"pattern_distance"	:	parse_int(v.find("pdist").text),
			"delayed"			:	True if v.find("dly") is not None else False
		}
	for v in root.findall('vehicle'):
		vehicles.append(parse_vehicle(v))
	return vehicles

def get_routes():
	params = {
		"key":keys.cta,
	}
	request_string = "getroutes"
	r = requests.get(base_url + request_string, params=params)
	r.encoding = "utf-8"
	root = ET.fromstring(r.text)
	routes = []
	def parse_route(r):
		return {
			"route"		:	r.find("rt").text,
			"route_name":	r.find("rtnm").text,
		}
	for r in root.findall('route'):
		routes.append(parse_route(r))
	return routes
print get_time()
print get_vehicles(vehicle_ids=['1567'])
print get_routes()