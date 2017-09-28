import hashlib
import sys
import json
import datetime as date
from helpers import findMerkleRoot

# define variables
version = "00000001"  # version

# define block class
class Block(object):
    def __init__(self, previous_hash=None, transactions=None):
        '''
            Constructor for Block class
              Block Header: Key info on block (80 bytes)
              Block Size: Size of the block (4 bytes)
              Transaction Count: Number of transactions (1-9 bytes)
              Transactions: Transactions in the block (variable size)

            Input:
                previous_hash - a hash of previous block
                transactions - a list of transactions included in block
                merkle_root - a hash of all the hashed transactions in the merkle tree

        '''

        # define block header attributes
        self.version = version.encode('utf8')  # 4 bytes
        self.previous_hash = previous_hash.encode('utf8')  # 32 bytes
        self.merkle_root() # 32 bytes
        self.block_timestamp()  # 4 bytes
        self.nonce = None  # 4 bytes
        self.target = None  # 4 bytes

        # define rest of block
        self.txcount = len(transactions) # 4 bytes
        self.transactions = transactions
        self.block_size()  # 4 bytes

    def block_size(self):
        # calculates the size of the block and sets instance size to value

    def block_timestamp(self):
        # gets the time and sets timestamp
        self.timestamp = str(date.datetime.now()).encode('utf8')

    def merkle_root(self):
        self.merkle_root = findMerkleRoot(self.transactions)

    def block_version(self, vers):
        # gets the version and updates that instance with the version

    def block_header(self):
        # returns the header info

    def hash(self, nonce=None):
        # calculates and returns the hash of the block
        # if nonce changes, update instance
        nonce = nonce or self.nonce

    @staticmethod
    def verify_hash(block_hash):
        # verifies the hash is valid by checking if it matches the criteria target difficulty

    def mine(self):
        # mines block by using pow to increment through nonce and if valid, block nonce is updated

    @staticmethod
    def get_merkle_root(transactions):
        # calculates the merkle root and returns the merkle_root of transactions
