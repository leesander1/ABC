""" Core Functions """
import os, json

from core.blocks.block import Block, genesis_block
from core.transaction.transaction import Transaction
from core.transaction.bundle_tx import bundle_tnx
from core.blocks.block_io import save_block
from core.configuration.configuration import Configuration

def mine():
    # config object
    conf = Configuration()
    # Mines blocks
    reward_address = conf.get_conf("wallet").get("address")
    reward_amount = conf.get_conf("reward")
    size = 0 # TODO: fix this
    # 2) bundle transactions
    tnx = bundle_tnx(size, reward_amount)

    b = Block(previous_hash=conf.get_conf("last_block"), transactions=tnx)
    Block.target(b, conf.get_conf("difficulty"))
    Block.mine(b)
    save_block(b)
    conf.increment_height()
    conf.update_previous_hash(b.block_hash())
    # 3) if success, save block, update db, update config with updated previous_hash & height
    # 4) notify network
    # 5) repeat
    return

def create_transaction(recipient, amount):
    """
    creates a new transaction and add it to verified_transactions.json
    :param recipient: public address of the recipient
    :param amount: the amount of abc to be sent
    :return: transaction
    """
    tx = Transaction()
    tx.add_output(recipient, amount)

    return tx

def add_to_verifiedPool(tx):
    verified_tx = (tx.get_transaction_id(), tx.get_data())
    try:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r') as file:
            data = json.load(file)
            file.close()
            data.update([verified_tx])

        # so that it overrides whatever is already in the verified_transactions.json
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            json.dump(data, file)
            file.close()
        return
    except IOError as e:
        print('{0}'.format(e))
    except ValueError:
        # TODO: Im pretty sure there is a better way to detect whether or not the file exist and add a new tx
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            data.update([verified_tx])
            json.dump(data, file)
            file.close()
