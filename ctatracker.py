import requests
import keys
from datetime import datetime
import xml.etree.ElementTree as ET

base_url = "http://www.ctabustracker.com/bustime/api/v1/"
	
def get_time():
	params = {"key":keys.cta}
	request_string = "gettime"
	r = requests.get(base_url + request_string, params=params)
	r.encoding = "utf-8"
	root = ET.fromstring(r.text)
	d = datetime.strptime(root.find('tm').text, '%Y%m%d %H:%M:%S')
	print d
get_time()
