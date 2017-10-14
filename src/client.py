from src.block import Block
from src.transaction import Transaction
import src.keybase as keys
import src.persistence as persist


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
    total = 0
    transaction = None
    my_address = persist.get_address()
    # get inputs
    unspent_transactions = persist.read_my_transactions()
    for tnx in unspent_transactions:
        for output in tnx.get_outputs():  # for each output
            if total < amount and output[1] == my_address:
                inputs.append(output)  # add this output as an input
                unspent_transactions.remove(tnx)
                total += output[2]  # add outputs value to total

    if total < amount:  # check to see if inputs are enough
        print("Insufficient Funds for {} abc transaction".format(amount))
    else:
        # update unspent transactions
        persist.overwrite_my_transactions(unspent_transactions)

        # create outputs
        outputs.append((rec_address, my_address, amount))
        total -= amount
        if total != 0:
            outputs.append((my_address, my_address, total))
        # build the transaction object
        transaction = Transaction(sender_pubkey=keys.get_public(),
                                  inputs=inputs,
                                  outputs=outputs,)
        transaction.sign(keys.get_private())
    return transaction


def send_transaction(rec_address, amount):
    """
    Send a transaction over the network.
    :param rec_address: the address of the receiver
    :param amount: the amount to the receivers address
    """
    tnx = create_transaction(rec_address, amount)
    # TODO: actually send over network
    print("Sending Transaction: {}".format(tnx))
    return tnx


def create_genesis():
    """
    Create a genesis block (the first block in the block chain)
    :return: a new Block object
    """
    data = {  # one transaction
        0:  {
                "id": "",  # TODO: hash of message
                "signature": "need_signature",  # TODO: one time key pair for genesis tnx
                "sender_pubkey": "need_public",  # TODO: one time key pair for genesis
                "message": {
                    "inputs": [
                        ("null", "genesis", 7000),
                        ("null", "genesis", 7000),
                        ("null", "genesis", 7000),

                    ],
                    "outputs": [
                        ("genesis", "kevin", 7000),
                        ("genesis", "dane", 7000),
                        ("genesis", "lee", 7000),
                    ]
                }
            }
    }
    return Block(index=0, data=data, previous_hash="0")