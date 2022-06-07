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
    """
    Description:
        Pins the file to IPFS.

    Parameters:
        * file: the file to be uploaded.

    Returns:
        The hash of the file that was uploaded.
    """

    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files = { "file": file },
        headers = file_headers
    )

    print(r.json())
    return r.json()["IpfsHash"]


def pin_json_to_ipfs(json):
    """
    Description:
        Pins the json file to IPFS.

    Parameters:
        * json: the json file to be uploaded.

    Returns:
        The hash of the file that was uploaded.
    """

    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data = json,
        headers = json_headers
    )

    print(r.json())
    return r.json()["IpfsHash"]


def retrieve_file_from_ipfs(hash, get_json = True):
    """
    Description:
        Gets the file from Pinata using the provided hash. Set get_json to true to receive the return message as 
        a json file, else the raw content will be returned.

    Parameters:
        * hash: the hash of the file to retrieve from Pinata.
        * get_json: will return the contents as a json if true, otherwise the raw content if false.

    Returns:
        The json or raw file from Pinata.
    """

    url = f"https://gateway.pinata.cloud/ipfs/{hash}"
    r = requests.get(url)

    if get_json:
        print(r.json())
        return r.status_code, r.json()
    else:
        return r.status_code, r.content