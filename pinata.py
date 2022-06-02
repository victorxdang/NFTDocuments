import json
import requests
import os

from dotenv import load_dotenv

load_dotenv()

# these two headers will be sent as part of the request for uploading to Pinata
json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY")
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_KEY")
}


def pin_file_to_ipfs(file):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files = { "file": file },
        headers = file_headers
    )

    print(r.json())
    return r.json()["IpfsHash"]


def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data = json,
        headers = json_headers
    )

    print(r.json())
    return r.json()["IpfsHash"]


def retrieve_file_from_ipfs(hash, get_json = False):
    url = f"https://gateway.pinata.cloud/ipfs/{hash}"
    r = requests.get(url)

    if get_json:
        print(r.json())
        return r.json()
    else:
        return r