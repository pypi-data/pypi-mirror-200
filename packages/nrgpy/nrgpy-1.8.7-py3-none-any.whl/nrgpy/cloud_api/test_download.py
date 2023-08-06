import getpass
import json
import os
from socket import gethostname
from sys import platform
import sys

try:
    import requests
except ImportError:
    import pip

    pip.main(["install", "--user", "requests"])
    import requests


## save folder
username = getpass.getuser()
hostname = gethostname()

if platform == "win32":
    home_dir = f"C:/Users/{username}"
else:
    home_dir = f"/home/{username}"

save_folder = home_dir

## api url
api_url = "http://localhost:7071/api/documents/downloadfolder"
# api_url = "https://nrgcloudapi.azure-api.net/customerapi/documents/downloadfolder"

## call api
folder_id = 1282
headers = {"content-type": "application/zip"}
resp = requests.get(
    url=f"{api_url}?folderId={folder_id}",
    headers=headers,
    stream=True,
)

## download result
filepath = os.path.join(home_dir, f"folderId_{folder_id}.zip")
if resp.status_code == 200:
    total = int(resp.headers.get("content-length", 0))
    dl = 0
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=10248):
            if chunk:
                f.write(chunk)

## print OK if no exceptions
print("ok, no exceptions")
print(f"file saved at {filepath}")
