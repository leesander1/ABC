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

def find_utxo(id, index):
    ensure_data_dir()

    ensure_data_dir()
    try:
        file = open(_PATH_UNSPENT_TNX, 'r')
        utxos = json.loads(file.read())
        print(utxos)
    except FileNotFoundError:


    return utxos
