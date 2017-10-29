from persist import abc_key as keys
from persist import block_chain
from block import Block
from transaction import Transaction


def create_transaction(rec_address, amount):
    """
    Initialize a Transaction object with a receiving address and amount
    :param rec_address: the recipient address
    :param amount: the amount to the recipient
    :return: the new Transaction object
    """
    transaction = Transaction()
    transaction.add_output(rec_address, amount)
    return transaction


def send_transaction(transaction):
    """
    Send a transaction over the network
    :param transaction: the Transaction object
    :return: 
    """
    transaction.unlock_inputs(keys.get_private_key(), keys.get_public_key())
    transaction.verify()
    # TODO: actually send over network
    print("Sending Transaction: {}".format(transaction.get_data()))
    return transaction


def create_genesis():
    """
    Create a genesis block (the first block in the block chain)
    :return: a new Block object
    """

    genesis_transaction = Transaction.create_genesis_transaction(keys.get_private_key(),
                                                        keys.get_public_key())
    data = [genesis_transaction.get_data()]
    block = Block(index=0, data=data, previous_hash="0")
    block_chain.write_block(block)
    return block
