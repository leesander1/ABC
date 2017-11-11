""" returns verified transactions """
import json
import os

from core.transaction.transaction import Transaction
from core.configuration.configuration import Configuration
from core.wallet.wallet import get_private_key, get_public_key

def bundle_tnx(size, reward_amount):
    """
    pull some verified transactions
    :param size: the amount of transaction to return
    :param cbtx: the coinbase transaction to add to the list of transactions
    :return: dict of transactions
    """
    cbx = create_coinbase_tx(reward_amount)
    block_transactions = {cbx.get_transaction_id(): cbx.get_data()}

    try:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r') as file:
            data = json.load(file)
            file.close()
    except IOError:
        print("~~~~~~~~~~~~~~~~")
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            json.dump(data, file)
            file.close()

    try:  # TODO: bundle as many transactions as possible
        tx_temp = []
        tx_temp.append(data.popitem())
        tx_temp.append(data.popitem())
        block_transactions.update(tx_temp)
    except KeyError as e:
        # there was not at least 2 transactions in verified_transactions.json
        print('Need at least 2 transaction per block\n{0}'.format(e))

    with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
        json.dump(data, file)
        file.close()

    return block_transactions


def create_coinbase_tx(reward_amount):
    """
    Create a new transaction where the output is the client's public key
    Will create a coinbase transaction
    :return: new transaction following a coinbase protocol
    """
    cbtx = Transaction()
    config = Configuration()
    cbtx.add_coinbase_output(get_public_key("string"), reward_amount)
    return cbtx