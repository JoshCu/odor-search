# import requests
# import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
# load the environment variables

atlas_api_key = os.environ.get("ATLAS_API_KEY")
url = "https://data.mongodb-api.com/app/data-dpfbx/endpoint/odor_search"

payload = {"search_term": "vani"}
headers = {
    'api-key': atlas_api_key,
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
