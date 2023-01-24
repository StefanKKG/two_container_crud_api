# This delete request deletes the data from row 1 from the database.
# To delete a different row of data, change the integer for the
#   row_id at the end of the BASE url.

# BASE URL syntax = https://127.0.0.1:5001/api/v1/read/{row_id}

import requests
BASE = "http://127.0.0.1:5001/api/v1/deleteperson/500"
response = requests.delete(BASE)
print(response.json())
