import hashlib as hasher
import datetime as date
import json


class Block(object):
    def __init__(self, **kwargs):
        """
        Create a block object
        :param index: the block height (previous block index + 1)
        :param data: a json serializable python dictionary of transactions
                    contained in this block. 
        :param previous_hash: the previous blocks hash
        """
        self.index = kwargs.pop('index')  # block height required
        self.previous_hash = kwargs.pop('previous_hash')  # previous block hash required3

        self.timestamp = kwargs.pop('timestamp', None)  # TODO: comput when POW is solved
        self.data = kwargs.pop('data', None)  # transactions as nested python dictionary
        self.hash = kwargs.pop('hash', None)  # TODO: compute when POW is solved

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
        new_data = data
        new_prev_hash = self.hash
        return Block(index=new_idx, data=new_data, previous_hash=new_prev_hash)



    def __str__(self):
        return json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "hash": self.hash,
            "previous_hash": self.previous_hash
        })
