from persist import abc_key as keys
from persist import block_chain
from block import Block
from transaction import Transaction


def send_transaction(rec_address, amount):
    """
    Send a transaction over the network
    :param transaction: the Transaction object
    :return: 
    """
    transaction = Transaction()
    try:
        transaction.add_output(rec_address, amount)
        public = keys.get_public_key()
        private = keys.get_private_key()
        transaction.unlock_inputs(private_key=private, public_key=public)
        transaction.verify()
        # TODO: actually send over network
        print("Sending Transaction: {}".format(transaction.get_data()))
    except ValueError as e:
        print(e)


def get_balance():
    return block_chain.get_my_balance()


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
