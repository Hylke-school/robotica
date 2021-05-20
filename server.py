import time
from get_json import JSON
import requests


json = JSON()

while True:
    payload = json.get_json()
    # if payload != "":
    #     print(payload)
    r = requests.post("http://dns.hylke.xyz:5356", data=payload)
    time.sleep(0.1)
