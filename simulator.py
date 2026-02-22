import requests
import random
import time

API_URL = "http://127.0.0.1:8000/api/telemetry/"

while True:
    data = {
        "speed": random.randint(40, 120),
        "fuel_level": random.randint(10, 100),
        "temperature": random.randint(60, 110),
        "latitude": 17.3850 + random.uniform(-0.01, 0.01),
        "longitude": 78.4867 + random.uniform(-0.01, 0.01)
    }

    try:
        response = requests.post(API_URL, json=data)
        print("Sent:", response.json())
    except Exception as e:
        print("Error:", e)

    time.sleep(5)