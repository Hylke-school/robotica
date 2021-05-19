import time
from get_json import JSON


json = JSON()

while True:
    # payload = json.get_json()
    json.start()
    # if payload != "":
    #     print(payload)
    # r = requests.post("http://dns.hylke.xyz:5356", data=payload)
    time.sleep(0.1)
