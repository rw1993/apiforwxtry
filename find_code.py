import requests
import hashlib
import numpy as np
import string
import random
import json

while True:
    latest = requests.get("http://127.0.0.1:5000/latest_code").text
    latest = json.loads(latest)
    latest_code = latest["code"]
    latest_id = latest["id"]
    while True:
        code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        guess = "{}{}".format(latest_code, code)
        guess_hash = hashlib.sha256(guess.encode()).hexdigest()
        if guess_hash[-1] == "0":
            anser = requests.post("http://127.0.0.1:5000/get_coin",
                          data={"user_id": "weiyanjie1",
                                "try_code": code,
                                "block_id": latest_id})
            import ipdb; ipdb.set_trace()
            break
