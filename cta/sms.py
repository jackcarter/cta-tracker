import os
import request

sms_url = os.environ.get('SENDHUB_URL')

def send_sms(number, sms_text):
	requests.post(sms_url,
		data='{"contacts":["%(number)s"],"text":"%(sms_text)s"}' \
		% {"number": number, "sms_text": sms_text})