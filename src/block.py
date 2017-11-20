from Crypto.Hash import SHA256
import datetime as date


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
            self.transactions = self.payload['transactions']
            self.hash = self.payload['hash']
        else:  # creating new block
            self.index = kwargs.pop('index')
            self.previous_hash = kwargs.pop('previous_hash')
            self.transactions = kwargs.pop('transactions')
            self.timestamp = None  # set timestamp when POW solved
            self.hash = None  # hash_block() when POW is solved
            self.mine_block()

    def hash_block(self):
        """
        Hash all contents of a Block using SHA256
        :return: string hexadecimal representation of the hashed block
        """
        payload = str(self.index) + \
                  str(self.timestamp) + \
                  str(self.transactions) + \
                  str(self.previous_hash)
        block_hash = SHA256.new(payload.encode('utf-8'))
        return block_hash.hexdigest()

    def mine_block(self):
        """
        Mine the block (POW)
        """
        # TODO: implement POW algorithm

        # set final properties after mined
        self.timestamp = date.datetime.now()
        self.hash = self.hash_block()

    def get_transactions(self):
        """
        Get all transactions in this block
        :return: a nested python dictionary containing all transactions in this
                 block
        """
        return self.transactions

    def get_hash(self):
        """
        Get the hash of this block
        :return: the hash as a string
        """
        return self.hash

    def get_previous_hash(self):
        """
        Get the previous hash of this block
        :return: the previous hash as a string
        """
        return self.previous_hash

    def get_next_block(self, transactions):
        """
        Create a new block based off of self.
        :param transactions: a nested python dictionary containing all transactions
                    for the new block
        :return: the newly created block
        """
        new_idx = self.index + 1
        new_data = transactions
        new_prev_hash = self.hash
        return Block(index=new_idx, transactions=new_data, previous_hash=new_prev_hash)

    def get_data(self):
        """
        get a dict representation of the entire Block object
        :return: dict of Block object
        """
        return {
            "index": self.index,
            "timestamp": str(self.timestamp),
            "transactions": self.transactions,  # should be a transaction as a dict
            "hash": self.hash,
            "previous_hash": self.previous_hash
        }
