from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import json
import os


class Transaction(object):
    def __init__(self, **kwargs):
        """
        
        :param kwargs: 
        """
        self.sender_pubkey = kwargs.pop('sender_pubkey')  # public key of sender in transaction
        self.id = kwargs.pop('id', None)
        self.signature = kwargs.pop('signature', None)  # signature of transaction
        self.message = kwargs.pop('message', None)  # inputs + outputs of transaction

        if self.message:
            self.inputs = self.message['inputs']  # (sender0, sender1, amount) of transaction
            self.outputs = self.message['outputs']  # (sender1, receiver, amount) of transaction

    def get_outputs(self):
        return self.outputs

    def get_inputs(self):
        return self.inputs

    def set_message(self, inputs, outputs):
        self.message = {"inputs": inputs, "outputs": outputs}

    def set_sender(self, pubkey):
        self.sender_pubkey = pubkey

    def generate_id(self):
        payload = str(self.message) + str(self.sender_pubkey)
        self.id = SHA256.new(payload.encode('utf-8')).hexdigest()

    def sign(self, sender_privkey):
        hashed_message = SHA256.new(str(self.message).encode('utf-8'))
        signer = DSS.new(sender_privkey, 'fips-186-3')
        signature = signer.sign(hashed_message)
        self.signature = signature

    def verify(self):
        hashed_message = SHA256.new(str(self.message).encode('utf-8'))
        verifier = DSS.new(self.sender_pubkey, 'fips-186-3')
        try:
            verifier.verify(hashed_message, self.signature)
            authentic = True
        except ValueError:
            authentic = False
        return authentic

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "sender_pubkey": str(self.sender_pubkey),
            "signature": str(self.signature),
            "message": self.message
        })