# This patch request updates the specified parameters of row 1 in the database.
# To update the parameters of a different row of data, change the integer for the
#   row_id at the end of the BASE url.

# The keys that you need to use in the payload object are the column
#  names of the Customers table which are "name", "phone", "email",
#  "address", "postalZIP", "region", "country".

# IMPORTANT: All of the keys and values of the payload object need to
#   be in string format because the csv sample data that is used
#   is in string format even when the fields should be integers.

# BASE URL syntax = https://127.0.0.1:5001/api/v1/updateperson/{row_id}

import requests
import json

payload = {
    "name": "New name",
    "phone": "000-000-0000",
    "address": "123 Street RD"
}

headers = {'content-type': "application/json"}
BASE = "http://127.0.0.1:5001/api/v1/updateperson/500"
response = requests.patch(BASE, data=json.dumps(payload), headers=headers)
print(response.text)
