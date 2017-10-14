from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
import json
import os


class Transaction(object):
    def __init__(self, **kwargs):
        """
        Instantiate a Transaction object from the network, a file, or by 
        by building a new transaction.
        :param **kwargs: arguments passed as key:value pair, can contain:
        
            :payload: payload is passed in from the network or from a file
                      and contains a JSON object (Python dict) representation
                      of a transaction. All information necessary to build a
                      Transaction object is in the payload object.
        
            OR
        
            :sender_pubkey: this node's public key 
            :inputs: a list of tuples representing all inputs
                     for this transaction. Only used when creating a new
                     transaction.
            :outputs: a list of tuples representing all outputs for
                      this transaction. Only used when creating a new 
                      transaction.
        """

        self.payload = kwargs.pop('payload', None)
        if self.payload:  # un-packing transaction from network or file
            self.sender_pubkey = self.payload['sender_pubkey']
            self.message = self.payload['message']
            self.id = self.payload['id']
            self.signature = self.payload['signature']
        else:  # building transaction
            self.signature = None
            self.sender_pubkey = kwargs.pop('sender_pubkey')
            self.message = {"inputs": kwargs.pop('inputs'),
                            "outputs": kwargs.pop('outputs')}
            self.id = SHA256.new(  # hash message + sender public key
                (str(self.message) +
                 self.sender_pubkey)
                    .encode('utf-8')).hexdigest()  # string format

    def get_outputs(self):
        """
        Get all outputs for this transaction
        :return: a list of tuples (sender, receiver, amount)
        """
        return self.message['outputs']

    def get_inputs(self):
        """
        Get all inputs for this transaction
        :return: a list of tuples (sender, receiver, amount)
        """
        return self.message['inputs']

    def get_id(self):
        """
        Get the transaction id
        :return: an SHA256 hash of message + sender public key in string
                 hexadecimal format
        """
        return self.id

    def sign(self, sender_private_key):
        """
        Sign a transaction using the Elliptic Curve Cryptographic method,
        using this node's private key and a SHA256 hashed message
        :param sender_private_key: ECC private key object for this node
        :return: 
        """
        hashed_message = SHA256.new(str(self.message).encode('utf-8'))
        signer = DSS.new(sender_private_key, 'fips-186-3')
        signature = signer.sign(hashed_message)
        self.signature = signature

    def verify(self):
        """
        Verify a transaction using the transactions signature, SHA256 hashed
        message, and ECC public key object of the sender's public key
        :return: boolean of if the transaction is authentic or not (True
                 if it is)
        """
        hashed_message = SHA256.new(str(self.message).encode('utf-8'))
        ecc_key = ECC.import_key(self.sender_pubkey)
        verifier = DSS.new(ecc_key, 'fips-186-3')
        try:
            verifier.verify(hashed_message, self.signature)
            authentic = True
        except ValueError:
            authentic = False
        return authentic

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "sender_pubkey": self.sender_pubkey,
            "signature": str(self.signature),
            "message": self.message
        })
