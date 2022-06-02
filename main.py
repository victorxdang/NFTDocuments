import os
import json
import streamlit as st

from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, retrieve_file_from_ipfs

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_URI")))

# obtain all of the available ethereum accounts 
accounts = w3.eth.accounts


@st.cache(allow_output_mutation = True)
def load_contract():
    """
    Description:
        Loads the contract using the address provided in the .env file. 
        This function should only execute once per page load.
    """
    with open(Path("./contracts/compiled/art_registry_abi.json")) as f:
        artwork_abi = json.load(f)
        
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = None

    if contract_address is not None:
        contract = w3.eth.contract(address = contract_address, abi = artwork_abi)

    return contract


def pin_file(filename, file, address):
    """
    Description:
        Upload the file to Pinata IPFS.

    Parameters:
        * filename: the name of the file.
        * file: the file to upload.
    """
    # pin the file to IPFS and get the address
    ipfs_file_hash = pin_file_to_ipfs(file.getvalue())

    # build metadata file for artwork
    token_json = {
        "name": filename,
        "image": ipfs_file_hash,
        "owner": address
    }

    # convert metadata to JSON data string that Pinata requires
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": token_json}

    # pin JSON using the address to IPFS
    json_ipfs_hash = pin_json_to_ipfs(json.dumps(data))

    return json_ipfs_hash


def retrieve_file(hash, address):
    json_data = retrieve_file_from_ipfs(hash)

    if json_data["owner"] == address:
        return json_data["name"], retrieve_file_from_ipfs(json_data["image"], False)
    else:
        return None, None


def get_existing_document():
    st.title("Get Existing Document")

    # have the user select the address to be used
    address = st.selectbox("Select Document Owner", options = accounts)

    # have the user input the pinned document hash
    file_hash = st.text_input("Document Hash:")

    st.markdown("---")

    if st.button("Get Document"):
        if file_hash is None or len(file_hash) == 0:
            st.write("Invalid file name! Enter a valid filename and try again.")
        else:
            name, file = retrieve_file(file_hash, address)

            if file is None:
                st.write("Could not retrieve image! Did you select the correct owner?")
            else:
                st.write("Document Info Retrieved:")
                st.write(f"Name: {name}")
                st.image(file.content)

        st.markdown("---")



def mint_new_documents():
    st.title("Mint Your Personal Documents")
    st.markdown("---")

    # have the user select the address to be used
    address = st.selectbox("Select Document Owner", options = accounts)
    st.markdown("---")

    # get the filename for this document
    filename = st.text_input("Document Name:")

    # get the document file
    file = st.file_uploader("Document File:", type = ["jpg", "jpeg", "png"])
    st.markdown("---")

    # upload the file and do proper null checks
    if st.button("Upload Document"):
        if filename is None or len(filename) == 0:
            st.write("Invalid file name! Enter a valid filename and try again.")
        elif file is None:
            st.write("No file uploaded! Please upload a file and try again.")
        else:
            #contract = load_contract()
            artwork_ipfs_hash = pin_file(filename, file, address)
            st.write("Upload Successful!\nSave this hash to access this document in the future!")
            st.write(artwork_ipfs_hash)

            uri = f"ipfs://{artwork_ipfs_hash}"
            #tx_hash = contract.functions.registerDocument(address, filename, uri).transact({
            #    "from": address,
            #    "gas": 1000000
            #})

            #receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            #st.write("Transaction receipt mined:")
            #st.write(dict(receipt))
            #st.write("Test Output")

        st.markdown("---")


# keys for the states to be used, done this way to eliminate typos
existing_document = "existing_document"
new_document = "new_document"


# checking if the keys exist and if not, save the keys with a default value
if existing_document not in st.session_state:
    st.session_state[existing_document] = False
if new_document not in st.session_state:
    st.session_state[new_document] = False


st.title("Select an Option To Get Started:")
st.markdown("---")

# allow the user to select either retrieving an existing document or minting a new document
if st.button("Get Existing Document"):
    st.session_state[existing_document] = True
    st.session_state[new_document] = False

if st.button("Mint New Document"):
    st.session_state[new_document] = True
    st.session_state[existing_document] = False

st.markdown("---")

# only call the appropriate function based on the button previously pressed
if st.session_state[existing_document]:
    get_existing_document()
elif st.session_state[new_document]:
    mint_new_documents()