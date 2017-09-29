import hashlib
import sys
import json
import datetime as date

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
        self.merkle_root = self.merkle_root()  # 32 bytes
        self.timestamp = self.block_timestamp()  # 4 bytes
        self.nonce = None  # 4 bytes
        self.target = None  # 4 bytes

        # define rest of block
        self.txcount = len(transactions)  # 4 bytes
        self.transactions = transactions  # NOTE: may need to change
        self.size = self.block_size()  # 4 bytes

    def block_size(self):
        # calculates the size of the block and returns instance size to value
        header = 80  # header is 80 bytes
        meta = 8  # the size and txcount are 8 bytes
        # TODO: Calculate the size of the transactions
        tx = 0
        block_size = header + meta + tx
        return block_size

    def block_timestamp(self):
        # gets the time and sets timestamp
        return str(date.datetime.now()).encode('utf8')

    def merkle_root(self):
        # calculates the merkle root and sets it as the blocks merkle_root
        return 0000000000000000000000000000000000000000000000000000000000000000

    def version(self, vers):
        # set the version
        self.version = vers

    def target(self, difficulty):
        # set the target difficulty
        self.target = difficulty

    def header(self):
        # returns the header info
        header = {
            'version': self.version,
            'parent': self.previous_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'target': self.target,
            'nonce': self.nonce
        }
        return header

    def info(self):
        # returns all the data of the block
        info = {
            'block': hash(self),
            'header': {
                'version': self.version,
                'parent': self.previous_hash,
                'merkle_root': self.merkle_root,
                'timestamp': self.timestamp,
                'target': self.target,
                'nonce': self.nonce
            },
            'txcount': self.txcount,
            'transactions': self.transactions,
            'size': self.size
        }
        return info

    def hash(self, nonce=None):
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

        return m.hexdigest()


    def verify_hash(self, block_hash):
        # verifies the hash is valid by checking if it matches the criteria target difficulty
        # 1) check if hash matches target difficulty
        prefix = ''
        prefix.zfill(self.target)  # prefix is a string of zeros of the target

        # return a boolean value
        # checks to see if hash starts with the prefix zeros
        return block_hash.startswith(prefix)

    def mine(self):
        # mines block by using pow to increment through nonce and if valid, block nonce is updated
        # n is the nonce count that will be incremented on each hash attempt
        nonce_try = self.nonce or 0

        # loop through, hash the block with the nonce and verify
        while True:
            hash_try = self.hash(nonce=nonce_try)  # hash the candidate block
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



