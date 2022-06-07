pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract File is ERC721Full {

    constructor () public ERC721Full("FileToken", "FT") {}

    struct Document{
        string name; // File name
        address owner; // owner of the file
    }

    mapping(uint256 => Document) public documentCollection;

    //event DocumentAdded(string name, string owner, string reportURI);

    function mintDocument (string memory name,
                            address owner,
                            string memory uri) public returns (uint256)
                            {
                                uint256 tokenId = totalSupply();

                                _mint(owner, tokenId);

                                _setTokenURI(tokenId, uri);

                                documentCollection[tokenId] = Document(name, owner);

                                return tokenId;
                            }
}