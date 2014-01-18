import requests
import keys

base_url = "http://www.ctabustracker.com/bustime/api/v1/gettime"
params = {"key":keys.cta}

r = requests.get(base_url, params=params)

print r.text