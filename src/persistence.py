from src.transaction import Transaction
from src.block import Block
import json
import os


_MY_ADDRESS_PATH = os.path.normpath('../data/my_address.txt')
_BLOCK_CHAIN_FILE_PATH = os.path.normpath('../data/block_chain.txt')
_UNSPENT_TRANSACTIONS_PATH = os.path.normpath('../data/unspent_transactions.txt')


def get_address():
    """
    Get this nodes address from a file. If the file does not exist,
    create it and write an address.
    :return: the address of this node
    """
    try:
        file = open(_MY_ADDRESS_PATH, 'r')
        address = file.read()
    except FileNotFoundError:  # create address file with address
        file = open(_MY_ADDRESS_PATH, 'wt')
        address = 'dane'
        file.write(address)
    file.close()

    return address


def write_block(block):
    """
    Append a new block to the end of the block chain by writing it to 
    end of block chain file
    :param block: the block object to append
    """
    # NOTE: this file path is static.
    # If the working directory isn't src/ it wont work
    # TODO: check index, previous hash before writing
    file = open(_BLOCK_CHAIN_FILE_PATH, 'a')
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
    file = open(_BLOCK_CHAIN_FILE_PATH, 'r')
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
    my_address = get_address()
    file = open(_UNSPENT_TRANSACTIONS_PATH, 'a')
    for i, transaction in block.get_transactions().items() :
        tnx = Transaction(payload=transaction)  # convert to Transaction object
        for output in tnx.get_outputs():
            if output[1] == my_address:  # receiver is position 1 of output
                file.write("{}\n".format(tnx))

    file.close()


def overwrite_my_transactions(transactions):
    """
    Overwrite all contents in the unspent transactions file
    :param transactions: the new list of unspent transactions
    """
    # TODO: this overwrites the entire file instead
    # TODO of just taking out the ones we used up. Maybe there is a better way
    file = open(_UNSPENT_TRANSACTIONS_PATH, 'wt')
    for tnx in transactions:
        file.write("{}\n".format(tnx))
    file.close()


def read_my_transactions():
    """
    Read in all saved unspent transactions addressed to this node
    :return: a list of transactions
    """
    try:
        file = open(_UNSPENT_TRANSACTIONS_PATH, 'r')
        transactions = [Transaction(payload=json.loads(x)) for x in file.readlines()]
        file.close()
    except FileNotFoundError:  # no transactions file found
        transactions = []
    return transactions
