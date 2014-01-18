import requests
import keys
import datetime
import xml.etree.ElementTree as ET

base_url = "http://www.ctabustracker.com/bustime/api/v1/"
	
def get_time():
	params = {"key":keys.cta}
	request_string = "gettime"
	r = requests.get(base_url + request_string, params=params)
	root = ET.fromstring(r.text)
	print root.find('tm').text
get_time()
