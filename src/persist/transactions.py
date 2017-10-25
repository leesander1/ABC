from src.transaction import Transaction
import json
import os

# private constant file paths
_PATH_UNSPENT_TNX = os.path.normpath('../data/utxos.txt')


def ensure_data_dir():
    """
    Check to see if the data directory exists.
    If not, create it
    """
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):  # check for existence
        os.mkdir(data_dir)  # create

def write_utxo(transaction):
    ensure_data_dir()

    file = open(_PATH_UNSPENT_TNX, 'a')
    file.write("{}\n".format(json.dumps(transaction.get_data())))
    file.close()

def find_utxo(input_id, output_index):
    """
    Find an unspent transaction output in the block chain
    :param input_id: the specified id of the transaction
    :param output_index: the specified unspent transaction output index
    :return: a dict representing the utxo containing the fields address,
            and amount
    """
    ensure_data_dir()

    return {}

def get_amount(amount):
    """
    Compose a list of unspent transaction outputs such that the sum of them
    is equal to or greater than `amount` from the list of unspent
    transaction outputs for this node
    :param amount: the amount to get
    :return: a list of uxo's as inputs and their totaling amount
    """
    return {}, 0
