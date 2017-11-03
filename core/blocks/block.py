import datetime as date
import hashlib
import json

from core.blocks.merkle import findMerkleRoot

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
        # calculates the merkle root and sets it as the blocks merkle_root
        return findMerkleRoot(transactions)

    def version(self, vers):
        # set the version
        self.version = vers

    def target(self, difficulty):
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
    'Mines the genesis block. (Always the same block) 0000b7efc7281627c3a296475b8e142e8a280ea34c22718e6fb16d8aa7a9423e'
    tnx = ['test1', 'test2', 'test3', 'test4', 'test5']
    b = Block(previous_hash='0000000000000000000000000000000000000000000000000000000000000000', transactions=tnx)
    Block.target(b, 4)
    Block.genesis_timestamp(b)
    Block.mine(b)
    return b

# if __name__ == '__main__':
#     # do something
