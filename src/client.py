from Crypto.PublicKey import ECC
from src.block import Block
from src.transaction import Transaction
from src.keybase import AbcKey
import src.network
import json
import os


MY_ADDRESS = None

MY_ADDRESS_PATH = os.path.normpath('../data/my_address.txt')
BLOCK_CHAIN_FILE_PATH = os.path.normpath('../data/block_chain.txt')
UNSPENT_TRANSACTIONS_PATH = os.path.normpath('../data/unspent_transactions.txt')

keys = AbcKey()


def get_address():
    """
    Get this nodes address from a file. If the file does not exist,
    create it and write an address.
    :return: 
    """
    try:
        file = open(MY_ADDRESS_PATH, 'r')
        address = file.read()
    except FileNotFoundError:  # create address file with address
        file = open(MY_ADDRESS_PATH, 'wt')
        address = 'dane'
        file.write(address)
    file.close()

    global MY_ADDRESS
    MY_ADDRESS = address


def write_block(block):
    """
    Append a new block to the end of the block chain by writing it to 
    end of block chain file
    :param block: the block object to append
    """
    # NOTE: this file path is static.
    # If the working directory isn't src/ it wont work
    # TODO: check index, previous hash before writing
    file = open(BLOCK_CHAIN_FILE_PATH, 'a')
    file.write("{}\n".format(block))
    file.close()


def read_block_chain(index=None):
    """
    Read block at index `index`. If no index is specified, the entire
    block chain is read.
    :param index: height of block to read
    :return: a list of Block object(s)
    """
    # TODO: This has to read the entire file in to a list object..
    # TODO: maybe there is a better way
    # NOTE: this file path is static.
    # If the working directory isn't src/ it wont work
    file = open(BLOCK_CHAIN_FILE_PATH, 'r')
    if index:
        blocks = [Block(**json.loads(x)) for x in file.readlines()[index]]
    else:
        blocks = [Block(**json.loads(x)) for x in file.readlines()]
    file.close()
    return blocks


def write_my_transactions(block):
    """
    Save all transactions in a block where MY_ADDRESS appears in the 
    receiving position of any of the outputs
    :param block: a Block object
    """
    file = open(UNSPENT_TRANSACTIONS_PATH, 'a')
    for i, transaction in block.get_transactions().items() :
        tnx = Transaction(payload=transaction)  # convert to Transaction object
        for output in tnx.get_outputs():
            if output[1] == MY_ADDRESS:  # receiver is position 1 of output
                file.write("{}\n".format(tnx))

    file.close()


def overwrite_my_transactions(transactions):
    """
    Overwrite all contents in the unspent transactions file
    :param transactions: the new list of unspent transactions
    """
    # TODO: this overwrites the entire file instead
    # TODO of just taking out the ones we used up. Maybe there is a better way
    file = open(UNSPENT_TRANSACTIONS_PATH, 'wt')
    for tnx in transactions:
        file.write("{}\n".format(tnx))
    file.close()


def read_my_transactions():
    """
    Read in all saved unspent transactions addressed to this node
    :return: a list of transactions
    """
    try:
        file = open(UNSPENT_TRANSACTIONS_PATH, 'r')
        transactions = [Transaction(payload=json.loads(x)) for x in file.readlines()]
        file.close()
    except FileNotFoundError:  # no transactions file found
        transactions = []
    return transactions


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
    # get inputs
    unspent_transactions = read_my_transactions()
    for tnx in unspent_transactions:
        for output in tnx.get_outputs():  # for each output
            if total < amount and output[1] == MY_ADDRESS:
                inputs.append(output)  # add this output as an input
                unspent_transactions.remove(tnx)
                total += output[2]  # add outputs value to total

    if total < amount:
        print("Insufficient Funds for {} abc transaction".format(amount))
    else:
        # update unspent transactions
        overwrite_my_transactions(unspent_transactions)

        # create outputs
        outputs.append((rec_address, MY_ADDRESS, amount))
        total -= amount
        if total != 0:
            outputs.append((MY_ADDRESS, MY_ADDRESS, total))
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