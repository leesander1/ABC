from Crypto.Hash import SHA256
import datetime as date
import json


class Block(object):
    def __init__(self, **kwargs):
        """
        Instantiate a Block object from the network, a file, or by 
        by building a new block.
        :param **kwargs: arguments passed as key:value pair, can contain:
            
            :payload: payload is passed in from the network or from a file
                      and contains a JSON object (Python dict) representation
                      of a block. All information necessary to build a Block
                      object is in the payload object.
                        
            OR
                        
            :index: index is passed in from get_next_block() only. It is
                    the index of the next created block on the chain. This
                    parameter is used only when creating a new block
            
            :data: data is passed in from get_next_block() only. It is the
                   user-supplied "data" consisting of all of the Transactions
                   to be included in the new block. This parameter is used
                   only when creating a new block
            
            :previous_hash: previous_hash is passed in from get_next_block()
                            only. It is the hash of the previous block on the
                            block chain. This parameter is used only when
                            creating a new block.
        """

        self.payload = kwargs.pop('payload', None)
        if self.payload:  # un-pack block from network or file
            self.index = self.payload['index']
            self.previous_hash = self.payload['previous_hash']
            self.timestamp = self.payload['timestamp']
            self.data = self.payload['data']
            self.hash = self.payload['hash']
        else:  # creating new block
            self.index = kwargs.pop('index')
            self.previous_hash = kwargs.pop('previous_hash')
            self.data = kwargs.pop('data')
            self.timestamp = None  # set timestamp when POW solved
            self.hash = None  # hash_block() when POW is solved

    def hash_block(self):
        """
        Hash all contents of a Block using SHA256
        :return: string hexadecimal representation of the hashed block
        """
        payload = str(self.index) + \
                  str(self.timestamp) + \
                  str(self.data) + \
                  str(self.previous_hash)
        hash = SHA256.new(payload.encode('utf-8'))
        return hash.hexdigest()

    def get_transactions(self):
        """
        Get all transactions in this block
        :return: a nested python dictionary containing all transactions in this
                 block
        """
        return self.data

    def get_next_block(self, data):
        """
        Create a new block based off of self.
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
