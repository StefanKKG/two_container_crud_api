# This PUT request inserts the data that is defined in the 'payload'
#   object into the database. 

# IMPORTANT: All of the keys and values of the payload object need to
#   be in string format because the csv sample data that is used
#   is in string format even when the fields should be integers.

# In the csv sample data, the postalZIP codes for example are
#   seperated by '-' which makes them strings not integers.


import requests
import json

payload = {
    "name": "Stefan Gunther",
    "phone": "305-444-4444",
    "email": "stefan@gmail.com",
    "address": "address 1",
    "postalZIP": "30333",
    "region": "North America",
    "country": "USA"
}

# This request gives me the "no name value provided" error
# when i run it with parser.parse_args()
headers = {'Content-Type': 'application/json'}
BASE = "http://127.0.0.1:5001/api/v1/createperson"
response = requests.put(BASE, data=json.dumps(payload),headers=headers)
print(response.json())
