""" Core Functions """
from core.blocks.block import Block, genesis_block
from core.transaction.transaction import Transaction
from core.transaction.bundle_tx import bundle_tnx
from core.blocks.block_io import save_block
from core.configuration.configuration import Configuration

def mine(conf):
    # config object
    conf = Configuration()
    # Mines blocks
    reward_address = conf["wallet"]["address"]
    reward_amount = conf["reward"]
    # 1) add coinbase tx with reward
    cbtx = {reward_address, reward_amount}

    # 2) bundle transactions
    tnx = bundle_tnx(cbtx)

    b = Block(previous_hash=conf["last_block"], transactions=tnx)
    Block.target(b, conf["difficulty"])
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
