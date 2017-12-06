""" Core Functions """
import json
import os

from Crypto.Hash import SHA256
from src.persist import save_block, save_unverified_transaction, save_verified_transaction, read_block, save_utxo
from src.block.block import Block, genesis_block, bundle_tnx
from src.configuration import Configuration
from src.transaction import Transaction
from src.wallet import get_public_key, get_private_key
from src.network import network


def mine():
    # config object
    conf = Configuration()
    # Mines block
    reward_address = conf.get_conf("wallet").get("address")
    reward_amount = conf.get_conf("reward")
    size = 0 # TODO: fix this
    # 2) bundle transactions
    tnx = bundle_tnx(size, reward_amount)

    b = Block(previous_hash=conf.get_conf("last_block"), transactions=tnx)
    b.set_target(conf.get_conf("difficulty"))
    b.mine()
    save_block(b)
    conf.increment_height()
    conf.update_previous_hash(b.block_hash())

    find_incoming_utxos(b.block_hash(), b.transactions)
    network.transmit(b.info(), "block")


def verify_block(b):
    # need to check txns
    conf = Configuration()
    bh = Block(payload=json.loads(b))
    save_block(bh)
    conf.increment_height()
    conf.update_previous_hash(bh.block_hash())


def create_transaction(recipient, amount):
    """
    creates a new transaction and add it to verified_transactions.json
    :param recipient: public address of the recipient
    :param amount: the amount of abc to be sent
    :return: None
    """
    # TODO: Send a success message to client
    conf = Configuration()
    try:
        tx = Transaction()
        tx.add_output(recipient, amount)
        tx.unlock_inputs(get_private_key(), get_public_key("string"))
        save_verified_transaction(tx.get_transaction_id(), tx.get_data())
        conf.subtract_balance(tx.sum_of_outputs())
    except ValueError as e:
        # Will raise if insufficient utxos are found
        raise ValueError("INSUFFICIENT FUNDS")

    network.transmit(json.dumps(tx.get_data()), "txn")

def get_block(block_hash):
    """
    Gets a block
    :param block_hash: the block hash
    :return: block
    """
    if block_hash == '':
        conf = Configuration()
        block_hash = conf.get_conf("last_block")
    return read_block(block_hash)


def init_configuration():
    """
    This will instantiate the config class
    and check if genesis block is created
    :return: configuration object
    """
    conf = Configuration()

    block_height = conf.get_conf("height")
    if block_height == 0:
        b = genesis_block()
        cwd = os.getcwd()
        try:
            os.makedirs(os.path.join(cwd, r'data'))
        except OSError as e:
            pass
        save_block(b)
        conf.increment_height()
        conf.update_previous_hash(b.block_hash())
        find_incoming_utxos(b.block_hash(), b.transactions, True)

    return conf


def find_incoming_utxos(block_hash, transactions, isGenesis=False):
    """
    Iterates through all the outputs and looks for any directed to user's wallet.
    If found, save to the utxo pool
    :return:
    """
    myAddress = SHA256.new(get_public_key("string").encode()).hexdigest()
    conf = Configuration()
    for tnx_id, tnx_info in transactions.items():
        # deserialize transaction
        tnx_payload = tnx_info
        tnx_payload["transaction_id"] = tnx_id
        tnx = Transaction(payload=tnx_payload)

        for index in range(len(tnx.outputs)):
            if tnx.outputs[index]["address"] == myAddress and not isGenesis:
                save_utxo(tnx.get_transaction_id(), index, block_hash, tnx.outputs[index]["amount"])
                conf.add_balance(tnx.outputs[index]["amount"])
            elif tnx.outputs[index]["address"] == myAddress and isGenesis:
                save_utxo(tnx.get_transaction_id(), -1, block_hash, tnx.outputs[index]["amount"])
                conf.add_balance(tnx.outputs[index]["amount"])


