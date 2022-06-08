pragma solidity ^0.5.0; // Version we are using, when compiling if any error change it to 0.5.0

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol"; // ERC721Full contract

contract File is ERC721Full {

    constructor() public ERC721Full("FileToken", "FT") {} // Takes the name of the file and the symbol of the file

    struct Document {

        string name; // File name
        address owner; // owner of the file
    }

    mapping(uint256 => Document) public documentCollection;


    /*event DocumentAdded(
        string memory name,
        address owner,
        string memory uri); */
    // Event to be fired when a document is added

    function mintDocument(
        string memory name, // Name of the document
        address owner, // Owner of the document
        string memory uri // URI of the document
    ) public returns (uint256) {
        // Returns the id of the document
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId); // Mints the document


        _setTokenURI(tokenId, uri); // Sets the URI of the document


        documentCollection[tokenId] = Document(name, owner); // Adds the document to the collection

        return tokenId; // Returns the id of the document
    }
}

