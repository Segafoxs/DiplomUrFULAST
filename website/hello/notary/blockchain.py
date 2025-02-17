from django.conf import settings
from web3 import Web3
from django.shortcuts import get_object_or_404, redirect


abi = [{"type":"function","name":"documentProofs","inputs":[{"name":"","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"findAndDelete","inputs":[{"name":"_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"payable"},{"type":"function","name":"findById","inputs":[{"name":"_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"tuple","internalType":"struct ProofOfExistence.DocumentProof","components":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}]}],"stateMutability":"view"},{"type":"function","name":"getAllDocumentProofs","inputs":[],"outputs":[{"name":"","type":"tuple[]","internalType":"struct ProofOfExistence.DocumentProof[]","components":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}]}],"stateMutability":"view"},{"type":"function","name":"notarize","inputs":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"removeNotarizedDocument","inputs":[{"name":"docId","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"removeSelectedDocuments","inputs":[{"name":"docIds","type":"uint256[]","internalType":"uint256[]"}],"outputs":[],"stateMutability":"nonpayable"}]


def get_block_number(number_tx):
    web3 = Web3(Web3.HTTPProvider(settings.ANVIL_URL))
    block = web3.eth.get_block(number_tx)
    return block

def get_block_pop(tx_hash, doc_id):
    dict_doc = {}

    web3 = Web3(Web3.HTTPProvider(settings.ANVIL_URL))

    result = web3.eth.get_transaction_receipt(tx_hash)


    dict_doc["block_number"] = result["blockNumber"]

    return dict_doc

def write_to_blockchain(doc_id, doc_hash, signature, public_key, user_name):
    web3 = Web3(Web3.HTTPProvider(settings.ANVIL_URL))

    # Create the contract instance
    contract = web3.eth.contract(address=settings.ANVIL_CONTRACT_ADDRESS, abi=abi)

    def notirize(doc_id, doc_hash, signature, public_key, user_name):
        tx_hash = contract.functions.notarize(doc_id, doc_hash, signature, public_key, user_name).transact({'from': web3.eth.accounts[0]})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        result = get_block_pop(tx_hash, doc_id)
        return result

    result = notirize(doc_id, doc_hash, signature, public_key, user_name)
    return result



def read_all_documents():
    web3 = Web3(Web3.HTTPProvider(settings.ANVIL_URL))

    # Create the contract instance
    contract = web3.eth.contract(address=settings.ANVIL_CONTRACT_ADDRESS, abi=abi)

    def get_all():
        return contract.functions.getAllDocumentProofs().call()

    return get_all()

def read_all_chain_by_doc_id(doc_id):
    web3 = Web3(Web3.HTTPProvider(settings.ANVIL_URL))

    # Create the contract instance
    contract = web3.eth.contract(address=settings.ANVIL_CONTRACT_ADDRESS, abi=abi)

    def get_by_doc_id():
        return contract.functions.findById(doc_id)

    return get_by_doc_id()
