"""

Sample heating agent that switches the heating on and off based on the thermostat state.

"""

import time
import requests

API_URL = "http://localhost:8080"
SLEEP = 10

# reset the simulation
response = requests.get(f"{API_URL}/reset")
response.raise_for_status()

while True:
    response = requests.get(f"{API_URL}/sensor")
    dict_data = response.json()
    temp = dict_data["value"]

    # get the thermostat state
    response = requests.get(f"{API_URL}/thermostat")
    thermostat = response.json()["value"]
    print(f"Current temperature: {temp}, Thermostat: {thermostat}")

    # switch the heating on or off based on the thermostat state
    if thermostat == True:
        response = requests.get(f"{API_URL}/heat-source/off")
    else:
        response = requests.get(f"{API_URL}/heat-source/on")

    time.sleep(SLEEP)
