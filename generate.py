#!/usr/bin/env python

from pg_storage import PgStorage
import defs
import random
import json
import requests


runners_count = 10

storage = PgStorage()

numbers = list(storage.names.keys())
numbers = random.sample(numbers, runners_count)
print(f"Going to send {runners_count} cards")
for number in numbers:
    card = {
        "stationNumber": 1,
        "cardNumber": number,
        "checkTime": defs.start,
        "startTime": defs.start,
        "finishTime": defs.deadline + random.randint(-100, 100),
        "punches": []
    }
    punch_count = random.randint(5, 23)
    dt = (card["finishTime"] - defs.start) // (punch_count + 1)
    random_codes = random.sample(list(range(31, 54)), punch_count)
    for idx, code in enumerate(random_codes):
        t = defs.start + dt * idx + random.randint(-(dt // 2), dt // 2)
        card["punches"].append({
            "cardNumber": number,
            "code": code,
            "time": t,
        })
    resp = requests.post(f"http://localhost:{defs.server_port}/card",
                         data=json.dumps(card))
    print(f"{number} -> {resp.status_code}")
