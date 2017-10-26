from persist.block_chain import read_all_blocks
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


def write_utxos(transactions_dict, public_key):
    """
    Write any transactions with outputs addressed to public_key
    :param transactions_dict: a list of transaction dicts
    :param public_key: the address to find transactions for
    :return: the amount of transaction outputs addressed to public_key
    """
    ensure_data_dir()
    transactions = [Transaction(payload=x) for x in transactions_dict]
    try:
        file = open(_PATH_UNSPENT_TNX, 'a')
        for transaction in transactions:
            my_outputs = transaction.get_outputs(public_key=public_key)
            # TODO: output payloads need to be index by index
            payload = {}
            for key, output in my_outputs.items():
                payload[key] = {"address": output['address'],
                             "amount": output['amount']}

                file.write("{}\n".format(
                    json.dumps({transaction.get_data(): payload})
                ))
        file.close()
    except FileNotFoundError:
        pass


def get_utxo(input_id, output_index):
    """
    Get a unspent transaction output from the unspent transactions file
    :param input_id: 
    :param output_index: 
    :return: 
    """
    return {}

def find_utxo(input_id, output_index):
    """
    Find an unspent transaction output in the block chain
    :param input_id: the specified id of the transaction
    :param output_index: the specified unspent transaction output index
    :return: a dict representing the utxo containing the fields address,
            and amount
    """
    ensure_data_dir()
    blocks = read_all_blocks()
    utxo = None
    block_count = len(blocks)
    i = 0
    while i < block_count and not utxo:  # loop through block chain
        transactions = [Transaction(payload=x) for x  # get all transactions
                        in blocks[i].get_transactions()]
        transaction_count = len(transactions)
        j = 0
        while j < transaction_count and not utxo:  # loop through transactions
            if input_id == transactions[j].get_transaction_id():
                # found our transaction
                utxo = transactions[j].get_outputs()[output_index]
            j += 1
        i += 1

    return utxo


def get_amount(amount):
    """
    Compose a list of unspent transaction outputs such that the sum of them
    is equal to or greater than `amount` from the list of unspent
    transaction outputs for this node
    :param amount: the amount to get
    :return: a list of utxo's as inputs and their totaling amount
    """

    try:
        file = open(_PATH_UNSPENT_TNX, 'r')
        unspent_transactions = [Transaction(payload=x) for x
                                in json.load(file.read())]
        file.close()
        total = 0
        utxos = []
        i = 0
        while total < amount:
            tnx = unspent_transactions[i]

    except FileNotFoundError:
        utxos = {}
        total = 0

    return utxos, total
