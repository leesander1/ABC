import base64

from Crypto.Hash import SHA256
from Crypto.Signature import DSS

from src.persist import get_unspent_outputs, find_unspent_output
from src.wallet import import_public_key, get_public_key


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
                [
                    {
                        transaction_id: # hash of previous transaction,
                        output_index: # index of referenced output,
                        unlock: {
                                    public_key: # full public key of sender
                                    signature: # signature of this transaction
                                }
                    },
                ]

            Transaction Output Structure:
                [
                       {
                            address: # hashed public key of recipient,
                            amount: # amount for this output
                        },
                ]

            Transaction structure:
                    id: {
                        input_count: # how many transaction inputs
                        inputs: # list of transaction input objects
                        output_count: # how many transaction outputs
                        outputs: # list of transaction output objects
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
            self.inputs = []
            self.output_count = 0
            self.outputs = []
            self.unused_amount = 0

    def add_output(self, address, amount):
        """
        Add a new output and necessary inputs to this transaction.
        Get enough currency by referencing previous unspent transaction outputs
        :param address: the public key address recipient
        :param amount: the amount to send
        :return: None
        """
        hash_address = SHA256.new(address.encode('utf-8')).hexdigest()

        if self.unused_amount >= amount:  # enough left over to cover output
            self.unused_amount -= amount
        elif self.unused_amount < amount:  # need to find more outputs
            find_amount = amount - self.unused_amount
            utxos, total = get_unspent_outputs(find_amount)
            self.input_count += len(utxos)
            self.inputs += utxos
            self.unused_amount = total - find_amount

        self.output_count += 1
        self.outputs.append({  # add new output
            "address": hash_address,
            "amount": amount
        })

    def add_coinbase_output(self, address, amount):
        """
        Adds an output to an address without having to verify inputs
        :param address: client's public key
        :param amount: amount to send
        :return: none
        """
        hash_address = SHA256.new(address.encode('utf-8')).hexdigest()

        self.output_count += 1
        self.outputs.append({  # add new output
            "address": hash_address,
            "amount": amount
        })

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
        if self.unused_amount != 0:  # use up all input amounts (change)
            hash_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
            self.outputs.append({
                "address": hash_address,
                "amount": self.unused_amount
            })
            self.output_count += 1
            self.unused_amount = 0

        for tnx_input in self.inputs:  # for each input
            utxo = find_unspent_output(tnx_input['transaction_id'],
                                       tnx_input['output_index'],
                                       tnx_input['block_hash'])
            if utxo:
                transaction_message = SHA256.new((  # compose message
                    str(tnx_input['transaction_id']) +
                    str(tnx_input['output_index']) +
                    str(utxo['address']) +  # hashed public key address
                    str(self.outputs)
                ).encode('utf-8'))
                signer = DSS.new(private_key, 'fips-186-3')
                signature = signer.sign(transaction_message)
                encoded = base64.b64encode(signature).decode()
                unlock = {  # create unlocking portion of the transaction
                    "public_key": public_key,
                    "signature": encoded
                }
                tnx_input['unlock'] = unlock  # assign to input.
            else:
                # TODO: raise error
                print("Invalid input found for {}".format(tnx_input))

    def verify(self):
        # TODO: Maybe rename this function to authenticate
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
        authentic = True
        for tnx_input in self.inputs:  # for each referenced input
            utxo = find_unspent_output(tnx_input['transaction_id'],
                                       tnx_input['output_index'],
                                       tnx_input['block_hash'])

            sig_key = SHA256.new(  # get this transaction's unlock public key
                tnx_input['unlock']['public_key'].encode()
            ).hexdigest()

            if sig_key == utxo['address']:  # if this node is the recipient of
                # the previous utxo
                transaction_message = SHA256.new((  # transaction message
                    str(tnx_input['transaction_id']) +  # input id
                    str(tnx_input['output_index']) +  # output index
                    str(utxo['address']) +  # hashed public key as address
                    str(self.outputs)
                ).encode('utf-8'))

                ecc_key = import_public_key(tnx_input['unlock']['public_key'])
                signature = tnx_input['unlock']['signature']
                decoded = base64.b64decode(signature.encode())
                verifier = DSS.new(ecc_key, 'fips-186-3')
                try:
                    verifier.verify(transaction_message, decoded)
                except ValueError:
                    authentic = False
                    break

        return authentic

    def get_transaction_id(self):
        """
        Calculate the transaction id. 
        :return: the transaction id of this transaction
        """
        transaction = self.get_data()
        txid = SHA256.new(
            str(transaction).encode()
        ).hexdigest()
        self.transaction_id = txid
        return txid

    def get_data(self):
        """
        Get a dict representation of a transaction with the
        transaction id as the key
        :return: a dict representation of the transaction object.
        This would typically be the value in a tx key-value
        """
        transaction = {
            "input_count": self.input_count,
            "inputs": self.inputs,
            "output_count": self.output_count,
            "outputs": self.outputs
        }
        return transaction

    def sum_of_outputs(self):
        """
        Calculates the sum of all outputs
        :return: Double
       """
        total = 0

        for output in self.outputs:
            total = total + output["amount"]
        return total

def create_coinbase_tx(reward_amount):
    """
    Create a new transaction where the output is the client's public key
    Will create a coinbase transaction
    :return: new transaction following a coinbase protocol
    """
    cbtx = Transaction()

    hashed_address = SHA256.new(get_public_key("string").encode()).hexdigest()
    cbtx.add_coinbase_output(hashed_address, reward_amount)
    return cbtx