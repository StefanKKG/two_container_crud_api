# This get request queries the data from row 1 from the database.
# To query a different row of data, change the integer for the 
#   row_id at the end of the BASE url.

# BASE URL syntax = https://127.0.0.1:5001/api/v1/read/{row_id}

import requests
import json

BASE = "http://127.0.0.1:5001/api/v1/getperson/500"
response = requests.get(BASE)
print (response.json())
