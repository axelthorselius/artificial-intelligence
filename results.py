import requests
import json

SERVER_ADRESS = "https://vilde.cs.lth.se/edap01-4inarow/"
API_KEY = 'nyckel'
# STIL_ID = ["ax744th-s"]
STIL_ID = ["vi3851gu-s"]

res = requests.post(SERVER_ADRESS + "stats",
                       data={
                           "stil_id": STIL_ID,
                           "api_key": API_KEY,
                       })

print(res.json())