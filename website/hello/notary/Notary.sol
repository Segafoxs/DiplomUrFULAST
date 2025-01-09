// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.5.4;
pragma experimental ABIEncoderV2;

/*
 *   Smart contract for notarizing documents
 */
contract ProofOfExistence {
    // Custom data struct to hold document object
    struct DocumentProof {
        uint256 docId; // Auto generated uint256 id
        bytes32 hashKey; // Auto generated hash using in-built object keccak256
        string documentHash;
        string signature; // Signature from user
        string userName; // User name who signed

    }
    // DocumentProof struct array to hold list of uploaded documents
    DocumentProof[] public documentProofs;

    //event DocumentProofAdded(uint256 docId, string document, bytes32 hashKey);
    event AllDocumentsEvent(DocumentProof[] documentProofs); //Registered event to through all documents

    //Function to notarize document
    // @Param - Document name, size and type
    // @Visibility - Public
    function notarize(
        uint256 docId,
        string memory documentHash,
        string memory signature,
        string memory userName
    ) public {
        // Condition to check if their's any document or not
        require(
            bytes(documentHash).length > 0,
            "Document hash should not be empty"
        );
        require(
            bytes(signature).length > 0,
            "Document signature should not be empty"
        );
        require(
            bytes(userName).length > 0,
            "User name should not be empty"
        );

        // Create documentProof object using user document object
        DocumentProof memory dp = DocumentProof(
            docId,
            generateProof(documentHash),
            documentHash,
            signature,
            userName
        );

        //push document into array
        documentProofs.push(dp);
        //Emit event
        emit AllDocumentsEvent(documentProofs);
    }

    // Function to remove single document
    // @Param - document id
    // @Retrun type - boolean if delete is success
    function removeNotarizedDocument(uint256 docId) public returns (bool) {
        return findAndDelete(docId);
    }

    // Function to remove bulk documents
    // @Param - list of document ids
    // @Visibility - Public
    function removeSelectedDocuments(uint256[] memory docIds) public {
        for (uint256 i = 0; i < docIds.length; i++) {
            findAndDelete(docIds[i]); // find and delete matched document
        }
    }

    //Function to retrieve all the document proofs
    //Visibility - Public
    //Return type - list of documents
    function getAllDocumentProofs()
        public
        view
        returns (DocumentProof[] memory)
    {
        return documentProofs;
    }

    //Internal function to notarize document
    //visibility - Pure and internal
    //Return type - Hash key (bytes32)
    function generateProof(string memory documentHash)
        internal
        pure
        returns (bytes32)
    {
        return keccak256(abi.encodePacked(documentHash));
    }

    //Function to find single document details
    //Param - document id
    //Visibility - view and public
    //return type - DocumentProof struct
    function findById(uint256 _id) public view returns (DocumentProof memory) {
        DocumentProof memory dp;
        //Loop documentProof array and returned the matched document
        for (uint256 i = 0; i < documentProofs.length; i++) {
            if (documentProofs[i].docId == _id) {
                dp = documentProofs[i];
                return dp;
            }
        }
        revert("Document does not exist.");
    }

    //Function to find document and delete based on document id
    // Visibility - Public and payable
    function findAndDelete(uint256 _id) public payable returns (bool) {
        uint256 docToDeleteIndex;
        //Find the index of document to be deleted
        for (uint256 i = 0; i < documentProofs.length; i++) {
            if (documentProofs[i].docId == _id) {
                docToDeleteIndex = i;
            }
        }
        //if not found revert
        if (docToDeleteIndex < 0) {
            revert("Document does not exist.");
        }
        //if document is at last index then delete and return true
        /*if (docToDeleteIndex == documentProofs.length) {
            documentProofs.length--;
            return true;
        } else {*/
            //Delete the document based on swap-swift logic
            DocumentProof memory lastIndexDoc = documentProofs[documentProofs
                .length - 1];


            DocumentProof memory toDeleteIndexDoc = documentProofs[docToDeleteIndex];
            documentProofs[docToDeleteIndex] = lastIndexDoc;
            documentProofs[documentProofs.length - 1] = toDeleteIndexDoc;

            return true;
        //}
    }
}