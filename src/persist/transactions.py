from src.transaction import Transaction
import json
import os

# private constant file paths
_PATH_UNSPENT_TNX = os.path.normpath('../data/received_transactions.txt')


def ensure_data_dir():
    """
    Check to see if the data directory exists.
    If not, create it
    """
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):  # check for existence
        os.mkdir(data_dir)  # create


def write_transaction(transactions):
    ensure_data_dir()
    pass


def read_all_transactions():
    ensure_data_dir()
    pass
