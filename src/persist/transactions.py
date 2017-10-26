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


def find_unspent_output(transaction_id, output_index, use_block_chain=False):
    """
    Find an unspent transaction output in either the block chain (for verifying
    transactions) or in the node's unspent transaction outputs file (for 
    creating new transactions)
    :param transaction_id: the id of the transaction containing the output
    :param output_index: the index of the output in the transaction
    :param use_block_chain: Search the block chain or not
    :return: 
    """
    ensure_data_dir()


def get_unspent_outputs(required_amount):
    """
    Gather unspent transaction outputs from this node's file for fulfilling
    new transaction inputs
    :param required_amount: minimum amount for the sum of the unspent outputs
    :return: a dict of unspent outputs and their total amount
    """
    ensure_data_dir()

