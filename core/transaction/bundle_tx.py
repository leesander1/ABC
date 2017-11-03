""" returns verified transactions """
import json
import os

from core.transaction.transaction import Transaction
from core.configuration.configuration import Configuration

def bundle_tnx(size, cbtx):
    """
    pull some verified transactions
    :param size: the amount of transaction to return
    :param cbtx: the coinbase transaction to add to the list of transactions
    :return: dict of transactions
    """
    cbx = create_coinbase_tx()
    block_transactions = {cbx.get_transaction_id(): cbx.get_data()}

    try:
        with open('{0}/verified_transaction.json'.format(os.path.join(os.getcwd(), r'data'))) as file:
            data = json.load(file)
            file.close()

            # TODO: bundle as many transactions as possible
            tx_temp = []
            tx_temp.append(data.popitem())
            tx_temp.append(data.popitem())
            block_transactions.update(tx_temp)

            json.dump(data)
            file.close()
    except IOError as e:
        # file does not exist or not able to read file
        print('{0}'.format(e))
    except KeyError as e:
        # there was not at least 2 transactions in verified_transactions.json
        print('Need at least 2 transaction per block\n{0}'.format(e))

    return block_transactions

def create_coinbase_tx():
    """
    Create a new transaction where the output is the client's public key
    Will create a coinbase transaction
    :return: new transaction following a coinbase protocol
    """
    cbtx = Transaction()
    config = Configuration()
    cbtx.add_coinbase_output(config.get_conf("key").get("public"), 50)
    return cbtx