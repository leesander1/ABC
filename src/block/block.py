import base64
import datetime as date
import hashlib
import json
import os

from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from src.block.merkle import findMerkleRoot
from src.transaction import Transaction, create_coinbase_tx
from src.wallet import get_private_key, get_public_key

# define variables
version = "00000001"  # version


class Block(object):
    def __init__(self, previous_hash=None, transactions=None, **kwargs):
        """
            Constructor for Block class
              Block Header: Key info on block (80 bytes)
              Block Size: Size of the block (4 bytes)
              Transaction Count: Number of transactions (1-9 bytes)
              Transactions: Transactions in the block (variable size)

            Input:
                previous_hash - a hash of previous block
                transactions - a list of transactions included in block
                merkle_root - a hash of all the hashed transactions in the merkle tree

        """
        self.payload = kwargs.pop('payload', None)
        if self.payload:
            # define block header attributes
            self.version = self.payload['header']['version'].encode('utf8')  # 4 bytes
            self.previous_hash = self.payload['header']['parent'].encode('utf8')  # 32 bytes
            self.merkle_root = self.payload['header']['merkle_root']  # 32 bytes
            self.timestamp = self.payload['header']['timestamp'].encode('utf8')  # 4 bytes
            self.nonce = self.payload['header']['nonce']
            self.target = self.payload['header']['target']

            # define rest of block
            self.transactions = self.payload['transactions']  # NOTE: may need to change
            self.txcount = self.payload['txcount']  # 4 bytes
            self.size = self.payload['size']
        else:
            # define block header attributes
            self.version = version.encode('utf8')  # 4 bytes
            self.previous_hash = previous_hash.encode('utf8')  # 32 bytes
            self.merkle_root = self.merkle_root(transactions)  # 32 bytes
            self.timestamp = self.block_timestamp()  # 4 bytes
            self.nonce = None  # 4 bytes
            self.target = None  # 4 bytes

            # define rest of block
            self.transactions = transactions  # NOTE: may need to change
            self.txcount = len(transactions)  # 4 bytes
            self.size = self.block_size()  # 4 bytes

    def block_size(self):
        # calculates the size of the block and returns instance size to value
        header = 80  # header is 80 bytes
        meta = 8  # the size and txcount are 8 bytes
        # TODO: Calculate the size of the transactions
        # for now assume each tx is 32 bytes
        tx = len(self.transactions) * 32
        block_size = header + meta + tx
        return block_size

    def block_timestamp(self):
        # gets the time and sets timestamp
        return str(date.datetime.now()).encode('utf8')

    def genesis_timestamp(self):
        # gets the time and sets timestamp
        self.timestamp = str("2017-10-08 13:18:06.810644").encode('utf8')

    def merkle_root(self, transactions):
        # calculates the merkle root and sets it as the block merkle_root
        return findMerkleRoot(list(transactions.keys()))

    def version(self, vers):
        # set the version
        self.version = vers

    def set_target(self, difficulty):
        # set the target difficulty
        self.target = difficulty

    def header(self):
        # returns the header info
        header = {
            'version': self.version.decode('utf-8'),
            'parent': self.previous_hash.decode('utf-8'),
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp.decode('utf-8'),
            'target': self.target,
            'nonce': self.nonce
        }
        return header

    def print_header(self):
        # pretty prints the header info
        print(json.dumps(self.header(), indent=4, sort_keys=True))
        return

    def info(self):
        # returns all the data of the block
        info = {
            'block': self.block_hash(self.nonce),
            'header': self.header(),
            'txcount': self.txcount,
            'transactions': self.transactions,
            'size': self.size
        }
        return info

    def print_info(self):
        # pretty prints the info json
        print(json.dumps(self.info(), indent=4, sort_keys=True))
        return

    def block_hash(self, nonce=None):
        # calculates and returns the hash of the block header
        # if nonce changes, update instance
        nonce = nonce or self.nonce

        # get the data to include in the message hash
        m = hashlib.sha256()
        m.update(self.version)
        m.update(str(self.previous_hash).encode('utf-8'))
        m.update(str(self.merkle_root).encode('utf-8'))
        m.update(str(self.timestamp).encode('utf-8'))
        m.update(str(nonce).encode('utf-8'))
        m.update(str(self.target).encode('utf-8'))
        return hashlib.sha256(m.hexdigest().encode('utf-8')).hexdigest()

    def verify_hash(self, block_hash):
        # verifies the hash is valid by checking if it matches the criteria target difficulty
        # 1) check if hash matches target difficulty
        prefix = ''
        prefix = prefix.zfill(self.target)  # prefix is a string of zeros of the target

        # return a boolean value
        # checks to see if hash starts with the prefix zeros
        # print(block_hash)
        return block_hash.startswith(prefix)

    def mine(self):
        # mines block by using pow to increment through nonce and if valid, block nonce is updated
        # n is the nonce count that will be incremented on each hash attempt
        nonce_try = self.nonce or 0

        # loop through, hash the block with the nonce and verify
        while True:
            hash_try = self.block_hash(nonce=nonce_try)  # hash the candidate block
            if self.verify_hash(hash_try):  # check to see if hash is valid
                # if true, we found the correct hash for the pow
                self.nonce = nonce_try  # set the nonce
                return
            else:  # was not correct a valid hash
                # increment the nonce_try
                nonce_try += 1

    def reset_nonce(self):
        # reset the nonce, should be reset after each block
        # for security reasons & simplicity
        self.nonce = None

    # @staticmethod
    # def get_merkle_root(transactions):
    #     # calculates the merkle root and returns the merkle_root of transactions
    #
    # @staticmethod
    # def tx_size(transactions):
    #     # calculates the size of the transactions


def genesis_block():
    'Mines the genesis block. (Always the same block)'
    tnx = create_genesis_transaction(get_private_key(), get_public_key("string"))
    tnx_id = tnx.get_transaction_id()
    tnx_payload = tnx.get_data()
    b = Block(previous_hash='0000000000000000000000000000000000000000000000000000000000000000', transactions={tnx_id: tnx_payload})
    Block.set_target(b, 4)
    Block.genesis_timestamp(b)
    Block.mine(b)
    return b


def create_genesis_transaction(private_key, public_key):
    # TODO: I don't think the genesis transaction needs inputs. It's the genesis, where is it getting its money from?
    """
    Create the genesis transaction.
    :param private_key:
    :param public_key:
    :return:
    """

    hashed_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
    transaction = {
        "input_count": 1,
        "inputs": [
            {
                "transaction_id": '',
                "output_index": -1,
                "unlock": {
                    "public_key": public_key,
                    "signature": '',
                }
            }
        ],
        "output_count": 1,
        "outputs": [
            {
                "address": hashed_address,
                "amount": 7000
            }

        ]
    }

    # fill the unlock signature
    transaction_message = SHA256.new((  # compose transaction message
        str(transaction['inputs'][0]['transaction_id']) +  # input id
        str(transaction['inputs'][0]['output_index']) +  # output index
        str(hashed_address) +  # hashed public key as address
        str(transaction['outputs'])
        # new outputs
    ).encode())
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(transaction_message)  # sign the message
    encoded = base64.b64encode(signature).decode()
    transaction['inputs'][0]['unlock']['signature'] = encoded

    transaction_id = SHA256.new(
        str(transaction).encode('utf-8')).hexdigest()
    transaction['transaction_id'] = transaction_id
    return Transaction(payload=transaction)

def bundle_tnx(size, reward_amount):
    """
    pull some verified transactions
    :param size: the amount of transaction to return
    :param cbtx: the coinbase transaction to add to the list of transactions
    :return: dict of transactions
    """
    cbx = create_coinbase_tx(reward_amount)
    block_transactions = {cbx.get_transaction_id(): cbx.get_data()}

    try:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r') as file:
            data = json.load(file)
            file.close()
    except IOError:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            json.dump(data, file)
            file.close()

    try:  # TODO: bundle as many transactions as possible
        tx_temp = []
        tx_temp.append(data.popitem())
        #tx_temp.append(data.popitem())
        block_transactions.update(tx_temp)

        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            json.dump(data, file)
            file.close()
    except KeyError as e:
        # there was not at least 2 transactions in verified_transactions.json
        print('Need at least 1 transaction per block')

    return block_transactions



