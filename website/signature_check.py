import gostcrypto
from web3 import Web3

if __name__ == '__main__':
    anvil_url = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(anvil_url))

    # Contract ABI
    # abi = [{"type":"function","name":"get","inputs":[],"outputs":[{"name":"","type":"uint256","internalType":"uint256"}],"stateMutability":"view"},{"type":"function","name":"set","inputs":[{"name":"x","type":"uint256","internalType":"uint256"}],"outputs":[],"stateMutability":"nonpayable"}]
    abi = [{"type":"function","name":"documentProofs","inputs":[{"name":"","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}],"stateMutability":"view"},{"type":"function","name":"findAndDelete","inputs":[{"name":"_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"payable"},{"type":"function","name":"findById","inputs":[{"name":"_id","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"tuple","internalType":"struct ProofOfExistence.DocumentProof","components":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}]}],"stateMutability":"view"},{"type":"function","name":"getAllDocumentProofs","inputs":[],"outputs":[{"name":"","type":"tuple[]","internalType":"struct ProofOfExistence.DocumentProof[]","components":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"hashKey","type":"bytes32","internalType":"bytes32"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}]}],"stateMutability":"view"},{"type":"function","name":"notarize","inputs":[{"name":"docId","type":"uint256","internalType":"uint256"},{"name":"documentHash","type":"bytes","internalType":"bytes"},{"name":"signature","type":"bytes","internalType":"bytes"},{"name":"publicKey","type":"bytes","internalType":"bytes"},{"name":"userName","type":"string","internalType":"string"}],"outputs":[],"stateMutability":"nonpayable"},{"type":"function","name":"removeNotarizedDocument","inputs":[{"name":"docId","type":"uint256","internalType":"uint256"}],"outputs":[{"name":"","type":"bool","internalType":"bool"}],"stateMutability":"nonpayable"},{"type":"function","name":"removeSelectedDocuments","inputs":[{"name":"docIds","type":"uint256[]","internalType":"uint256[]"}],"outputs":[],"stateMutability":"nonpayable"}]
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    # Create the contract instance
    contract = web3.eth.contract(address=contract_address, abi=abi)

    def get_all():
        return contract.functions.getAllDocumentProofs().call()


    if len(get_all()) == 0:
        exit(0)

    doc1 = get_all()[0]

    sign_obj = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                            gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                                'id-tc26-gost-3410-2012-256-paramSetB'])
    password = "6ODRMcRY1N2sXVNeh83UXCM10mjLU53L"
    private_key = bytearray(password, encoding="utf-8")
    public_key = sign_obj.public_key_generate(private_key)

    print(public_key)
    if sign_obj.verify(public_key, doc1[2], doc1[3]):
        print('Signature is correct')
    else:
        print('Signature is not correct')

    #print("Value after increment:", get_all())