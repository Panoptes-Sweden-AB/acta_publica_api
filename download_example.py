import requests
import json
import os

# Set the credentials as ENV variables or change them in code
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

# Base url
base_url = "https://api.arkivet.actapublica.se/"

# The script accepts multiple queries as a list of object. dir: directory to save the files, query: the search query, download: to save the files or not, size: the max number of results the query can have
queries = []
queries.append({"dir": "trdomar", "query": "+doctype:trdom", "download": True, "size": 100})
queries.append({"dir": "hrdomar", "query": "+doctype:hrdom", "download": True, "size": 100})

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

# create directory if not present
if not os.path.isdir("downloads"):
    os.mkdir("downloads")

# Loop through queries
for query in queries:
    if query['download']:
        if not os.path.isdir("downloads/" + query['dir']):
            os.mkdir("downloads/" + query['dir'])
        
    print("Dir: {dir} Query: {query}".format(dir=query['dir'], query=query['query']))
    res = requests.post(base_url + "search", json={"query": query['query'], "size": query['size']}, headers=generic_headers, timeout=120)
    results = json.loads(res.text)
    if 'hits' in results:
        for hit in results['hits']:
            if query['download']:
                if os.path.isfile("downloads/" +query['dir'] + "/" + hit['filename']):
                    print("Skip {file}".format(file="downloads/" +query['dir'] + "/" + hit['filename'], ))
                else:
                    download = requests.get(hit['document_download_link'], timeout=120)
                    try:
                        open("downloads/" + query['dir'] + "/" + hit['filename'], 'wb').write(download.content)
                    except:
                        print("Error on download")
                    print("Download {file}".format(file="downloads/" +query['dir'] + "/" + hit['filename'], ))
