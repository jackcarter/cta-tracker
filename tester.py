import ctatracker
import requests
import json

a = ctatracker.BusTracker()
'''
print a.get_time()
print a.get_vehicles(vehicle_ids=['1567'])
print a.get_routes()
print a.get_directions('49')

print a.get_stops('72','Eastbound')

print a.get_predictions(['17404'], top=1)
'''
headers = {'X-CSRFToken': '6zVWIyD92BNjkOeZUnh1Q7K6rH5m7nrq'}
payload = {'some': 'data'}
response = requests.post('http://localhost:8000/ajax/cta/echo.json', data=json.dumps(payload), headers=headers)

print dir(response)
print response.text