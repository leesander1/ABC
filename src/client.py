from persist import abc_key as keys
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
    inputs = []
    outputs = []

    # TODO: find inputs to this node
    # TODO: formulate outputs using inputs & amount
    # TODO: remove inputs from this node (avoid double spending)
    transaction = Transaction(sender_pubkey=keys.get_public_key(
        output='string'),
                              inputs=inputs,
                              outputs=outputs)

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
    inputs = [  # inputs (from, to, amount)
        ("null", "genesis", 21000),
    ]
    outputs = [  # outputs (from, to, amount)
        ("genesis", "kevin", 7000),
        ("genesis", "dane", 7000),
        ("genesis", "lee", 7000),
    ]
    tnx0 = Transaction(sender_pubkey="genesis",
                       inputs=inputs,
                       outputs=outputs)

    data = {0: tnx0.get_data()}
    return Block(index=0, data=data, previous_hash="0")
