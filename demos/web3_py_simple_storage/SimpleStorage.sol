// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;


contract SimpleStorage {

    uint256 favoriteNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber; 


    function store(uint256 _favoriteNumber) public returns(uint256){
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    //view, pure - reading the block chain doesn't cost gas
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    } 

    //memory: store it a time of execution  storage: store it forever.
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }


}
