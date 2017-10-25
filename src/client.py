from persist import abc_key as keys
from persist import transactions
from persist import block_chain
from block import Block
from transaction import Transaction, create_genesis_transaction


def create_transaction(rec_address, amount):
    """
    Create a transaction (gather inputs, outputs, and 
    format them into a Transaction object and then sign the transaction.
    :param rec_address: the address of the receiver
    :param amount: the amount to the receivers address
    :return: a complete filled out Transaction object
    """
    # TODO: find inputs to this node
    # TODO: remove inputs from this node (avoid double spending)
    transaction = Transaction(
        input_id='0',
        output_index='0',
        pubkey_script=rec_address,
        public_key=keys.get_public_key(output='string'),
        amount=amount
    )

    transaction.sign(keys.get_private_key())

    return transaction


def send_transaction(rec_address, amount):
    """
    Send a transaction over the network.
    :param rec_address: the address of the receiver
    :param amount: the amount to the receivers address
    """
    transaction = create_transaction(rec_address, amount)
    # TODO: actually send over network
    print("Sending Transaction: {}".format(transaction.get_data()))
    return transaction


def create_genesis():
    """
    Create a genesis block (the first block in the block chain)
    :return: a new Block object
    """

    # to use a utxo as an input above, the node's pubkey must match the utxo's
    # pubkey, and the pubkey must be used to verify the sig
    # the sig is the utxo's protected data () hashed together and signed by
    # the recepients private key.

    data = create_genesis_transaction(
        amount=7000,
        rec_address=keys.get_public_key(output='string'),
        private_key=keys.get_private_key()
    )
    block = Block(index=0, data=data, previous_hash="0")
    block_chain.write_block(block)
    return block
