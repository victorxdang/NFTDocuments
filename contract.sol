pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract File is ERC721Full {
    using Counters for Counters.Counter;
    Counter.Counter private _tokenIds;

    constructor () public ERC721Full("FileToken", "FT){}

    struct Document{
        string name; // File name
        string image; // ipsfs hash of the file
        string owner; // owner of the file
    }
    mapping(uint256 => Document) public documentCollection;

    event DocumentAdded(uint256 tokenId, string name, string image, string owner, string reportURI);

    function mintDocument (string memory name,
                            string memory image, 
                            address owner
                            uint256 tokenId,
                            string memory tokenURI) public returns (uint256)
                            {
                                uint256 tokenId = _tokenIds.current();

                                _mint(owner, tokenId);

                                _setTokenURI(tokenId, tokenURI);

                                documentCollection[tokenId] = Document(name, image, owner);
}
