import requests
import json
import os

# Set the credentials as ENV variables or change them in code
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

# Base url
base_url = "https://api.arkivet.actapublica.se/"

# The script accepts multiple queries as a list of object. dir: directory to save the files, query: the search query, download: to save the files or not, size: the max number of results the query can have

authorization = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "document.view,document.list,agent.detail,agent.list,document.download"
}

generic_headers = {
    "Content-Type":"application/json",
}

# Get authorization token
res = requests.post(base_url + "authorize", json=authorization, headers=generic_headers)
access_token = json.loads(res.text)
generic_headers['Authorization'] = access_token['token_type'] + " " + access_token['access_token']

query = {
    "query":"NOT äktenskapsskillnad",
    "size":"100",
    "page":"1",
    "start_date":"2-8-2019 00:00:00",
    "end_date":"2-8-2024 00:00:00",
    "personnummer":
        {
            "condition":"OR",
            "values":
                ["pnr1", "pnr2"]
        },
    "doctype":
        ["trdom","miljodom","migdom","krdom","hrdom","hdbeslut","frdom","hfdbeslut"],
        "datadoc":False
}
