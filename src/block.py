import hashlib as hasher
import datetime as date
import json


class Block(object):
    def __init__(self, index, data, previous_hash):
        """
        Create a block object
        :param index: the block height (previous block index + 1)
        :param data: a json serializable python dictionary of transactions
                    contained in this block. Transactions are labelled
                    by integer keys from 0 to n. Each transaction is a json
                    serializable python dictionary containing the fields
                    'inputs', and 'outputs'
        :param previous_hash: the previous blocks hash
        """
        self.index = index  # block height
        self.timestamp = date.datetime.now()  # time created
        self.data = data  # transactions as nested python dictionary
        self.previous_hash = previous_hash  # previous block hash
        self.hash = self.hash_block()  # compute this block hash

    def hash_block(self):
        sha = hasher.sha256()
        payload = str(self.index) + \
                  str(self.timestamp) + \
                  str(self.data) + \
                  str(self.previous_hash)

        sha.update(payload.encode('utf-8'))
        return sha.hexdigest()

    def get_transactions(self):
        """
        Get all transactions for this block
        :return: a nested python dictionary containing all transactions in this
                 block
        """
        return self.data

    def get_next_block(self, data):
        """
        Create a new block based off this one.
        :param data: a nested python dictionary containing all transactions
                    for the new block
        :return: the newly created block
        """
        new_idx = self.index + 1
        new_data = data  # TODO: needs data
        new_prev_hash = self.hash
        return Block(new_idx, new_data, new_prev_hash)

    @staticmethod
    def create_genesis():
        """
        Create a genesis block (the first block in the block chain)
        :return: 
        """
        data = {
            0: {
                "inputs": [
                    ("null", "genesis", 7000),
                    ("null", "genesis", 7000),
                    ("null", "genesis", 7000),

                ],
                "outputs": [
                    ("genesis", "kevin", 7000),
                    ("genesis", "dane", 7000),
                    ("genesis", "lee", 7000),
                ]
            }
        }
        return Block(0, data, "0")

    def __str__(self):
        return json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "hash": self.hash,
            "previous_hash": self.previous_hash
        })
