import time

import requests

from get_json import JSON

json = JSON()

payload = json.get_json()

while True:
    r = requests.post("dns.hylke.xyz:5356", data=payload)
    time.sleep(0.1)
