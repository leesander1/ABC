from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from persist.abc_key import import_public_key
from persist.transactions import find_utxo, get_amount


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
                      
                      
            Otherwise, it is assumed that a new transaction is being created,
            and subsequent calls to `Transaction().add_output()` are needed
            to fill the transaction, followed by `Transaction().unlock_inputs()`
            to complete the new Transaction.
        
        :notes
        
            Transaction Input Structure:
                    index: {
                        transaction_id: # hash of previous transaction,
                        output_index: # index of referenced output,
                        unlock: {
                                    public_key: # full public key of sender
                                    signature: # signature of this transaction
                                }
                    }
                    
            Transaction Output Structure:
                   index: {
                        address: # hashed public key of recipient,
                        amount: # amount for this output
                    }
                    
            Unspent Transaction Structure:
                   id: {
                        address: 
                        amount: 
                   }
                    
                    
            Transaction structure:
                    id: {
                        input_count: # how many transaction inputs
                        inputs: # dict of transaction input objects
                        output_count: # how many transaction outputs
                        outputs: # dict of transaction output objects
                    }
            
        """

        self.payload = kwargs.pop('payload', None)
        if self.payload:  # un-packing transaction from network or file
            self.transaction_id = self.payload['transaction_id']
            self.input_count = self.payload['input_count']
            self.inputs = self.payload['inputs']
            self.output_count = self.payload['output_count']
            self.outputs = self.payload['outputs']
        else:  # creating new transaction
            self.transaction_id = None
            self.input_count = 0
            self.inputs = {}
            self.output_count = 0
            self.outputs = {}
            self.unused_amount = 0

    def add_output(self, address, amount):
        """
        Add a new output to this transaction.
        Get enough currency by referencing previous unspent transaction outputs
        :param address: the public key address recipient
        :param amount: the amount to send
        :return: True if the output was added, false otherwise
        """

        success = False
        # if we have leftover from previous output we use it
        amount -= self.unused_amount  # subtract leftovers from previous outputs
        self.unused_amount = 0  # reset unused amount
        utxos, total = get_amount(amount)  # get inputs and their sum

        if total >= amount:
            # add the unspent transaction output as an input
            success = True
            self.unused_amount = total - amount  # calculate leftovers
            self.inputs[self.input_count] = utxos  # add utxos as inputs
            self.input_count += 1

            # create the new output
            hash_address = SHA256.new(address.encode('utf-8')).hexdigest()
            self.outputs[self.output_count] = {
                "address": hash_address,
                "amount": amount
            }
            self.output_count += 1

        return success

    def unlock_inputs(self, private_key, public_key):
        """
        Unlock previous unspent transaction outputs for a new transaction.
        Compose a transaction message consisting of:
            - input transaction ID
            - input output index
            - unspent transaction object's public key script (hashed pubkey)
            - this transaction's public key script (s)?
            - this transaction's output amount (s)?
        and sign it with this node's private key. 
        
        Place a dict consisting of {key: public_key, sig: signature} in the
        corresponding input at "unlock" where `public_key` is this node's
        full public key and `signature` is the signed transaction message.
        """
        # before unlocking, make sure we have used up all input amounts
        if self.unused_amount != 0:
            # create the new output, giving leftovers to the sender
            hash_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
            self.outputs[self.output_count] = {
                "address": hash_address,
                "amount": self.unused_amount
            }
            self.output_count += 1
            self.unused_amount = 0
        
        for tnx_input in self.inputs:  # for each input
            utxo = find_utxo(tnx_input['transaction_id'],  # get unspent tnx
                             tnx_input['output_index'])

            transaction_message = SHA256.new((  # compose transaction message
                str(tnx_input['transaction_id']) +  # input id
                str(tnx_input['output_index']) +  # output index
                str(utxo['address']) +  # hashed public key as address
                str(self.outputs)
            ).encode('utf-8')).hexdigest()
            signer = DSS.new(private_key, 'fips-186-3')
            signature = signer.sign(transaction_message)  # sign the message

            unlock = {  # create unlocking portion of the transaction
                "public_key": str(public_key),
                "signature": str(signature)
            }
            tnx_input['unlock'] = unlock  # assign to input.

    def verify(self):
        """
        Verify an incoming transaction.
            1) SHA256 hash the unspent transaction object's address
               and SHA256 hash this transaction's signature script key and
               see if they match. If they do, continue. Otherwise return false.
               
            2) Compose the transaction's message consisting of:
                - input transaction ID
                - input output index
                - unspent transaction object's public key script (hashed pubkey)
                - this transaction's public key script (s)?
                - this transaction's output amount (s)?
                and check to see if this transaction's signature can be 
                verified by the now authorized signature script key.             
                
        :return: True if the transaction is valid, false otherwise
        """
        authentic = False
        for tnx_input in self.inputs:  # for each referenced input
            utxo = find_utxo(tnx_input['transaction_id'],  # get unspent tnx
                             tnx_input['output_index'])

            sig_key = SHA256.new(  # get this transaction's unlock public key
                tnx_input['unlock']['public_key'].encode('utf-8')
            ).hexdigest()

            # TODO: what if they are different public keys but same private key?
            if sig_key == utxo['address']:  # if this node is the recipient of
                # the previous utxo
                transaction_message = SHA256.new((  # transaction message
                        str(tnx_input['transaction_id']) +  # input id
                        str(tnx_input['output_index']) +  # output index
                        str(utxo['address']) +  # hashed public key as address
                        str(self.outputs)
                ).encode('utf-8')).hexdigest()

                ecc_key = import_public_key(tnx_input['unlock']['public_key'])
                signature = tnx_input['unlock']['signature']
                verifier = DSS.new(ecc_key, 'fips-186-3')
                try:
                    verifier.verify(transaction_message, signature)
                    authentic = True
                except ValueError:
                    authentic = False
        return authentic

    def get_outputs(self, public_key=None):
        """
        Get a dict of transaction outputs that are sent to  `public_key`
        :param public_key: a full public key 
        :return: a dict of outputs 
        """
        if public_key:
            my_outputs = {}
            hash_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
            for key, output in self.outputs.items():
                if output['address'] == hash_address:
                    my_outputs[key] = output
        else:
            my_outputs = self.outputs
        return my_outputs

    def get_transaction_id(self):
        """
        Calculate the transaction id. 
        :return: the transaction id of this transaction
        """
        transaction = {
                "input_count": self.input_count,
                "inputs": self.inputs,
                "output_count": self.output_count,
                "outputs": self.outputs
            }
        txid = SHA256.new(
                str(transaction).encode('utf-8')
        ).hexdigest()
        self.transaction_id = txid
        return txid

    def get_data(self):
        """
        Get a dict representation of a transaction with the
        transaction id as the key
        :return: a dict representation of the transaction object with the 
                 transaction id as its key
        """
        txid = self.get_transaction_id()
        transaction = {
            "transaction_id": txid,
            "input_count": self.input_count,
            "inputs": self.inputs,
            "output_count": self.output_count,
            "outputs": self.outputs
        }
        return {txid: transaction}

    @staticmethod
    def _create_genesis_transaction(private_key, public_key):
        """
        Create the genesis transaction.
        :param private_key: 
        :param public_key: 
        :return: 
        """

        hashed_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
        transaction = {
            "input_count": 1,
            "inputs": {
                0: {
                    "transaction_id": '',
                    "output_index": -1,
                    "unlock": {
                        "public_key": public_key,
                        "signature": ''
                    }
                }
            },
            "output_count": 1,
            "outputs": {
                0: {
                    "address": hashed_address,
                    "amount": 7000
                }

            }
        }

        # fill the unlock signature
        transaction_message = SHA256.new((  # compose transaction message
            str(transaction['inputs'][0]['transaction_id']) +  # input id
            str(transaction['inputs'][0]['output_index']) +  # output index
            str(hashed_address) +  # hashed public key as address
            str(transaction['outputs'])  # new outputs
        ).encode('utf-8')).hexdigest()
        signer = DSS.new(private_key, 'fips-186-3')
        signature = signer.sign(transaction_message)  # sign the message
        transaction['inputs'][0]['unlock']['signature'] = signature

        transaction_id = SHA256.new(str(transaction)).hexdigest()
        return {transaction_id: transaction}





