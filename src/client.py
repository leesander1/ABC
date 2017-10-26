from persist import abc_key as keys
from persist import block_chain
from block import Block
from transaction import Transaction


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
    transaction = Transaction()

    transaction.add_output(rec_address, amount)
    return transaction.get_data()


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

    genesis_transaction = Transaction.create_genesis_transaction(keys.get_private_key(),
                                                        keys.get_public_key(output='string'))
    data = {genesis_transaction.get_transaction_id(): genesis_transaction.get_data()}
    block = Block(index=0, data=data, previous_hash="0")
    block_chain.write_block(block)
    block_chain.write_utxos(block.get_transactions(), keys.get_public_key(output='string'))
    return block
