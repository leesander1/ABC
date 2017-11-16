""" Core Functions """
import json
import os

from Crypto.Hash import SHA256
from src.persist import save_block, save_unverified_transaction, save_verified_transaction, read_block, save_utxo
from src.block.block import Block
from src.configuration import Configuration
from src.transaction import Transaction, bundle_tnx
from src.wallet import get_public_key, get_private_key


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
    :return: None
    """
    # TODO: Send a success message to client
    try:
        tx = Transaction()
        tx.add_output(recipient, amount)
        tx.unlock_inputs(get_private_key(), get_public_key("string"))
        save_verified_transaction(tx.get_transaction_id(), tx.get_data())
    except ValueError as e:
        raise ValueError("INSUFFICIENT FUNDS")

def get_block(block_hash):
    """
    Gets a block
    :param block_hash: the block hash
    :return: block
    """
    return read_block(block_hash)

def init_configuration():
    """
    This will instantiate the config class
    :return: configuration object
    """

    # TODO: Genesis block should be created here
    # TODO: Then call finc_incoming_utxos
    return Configuration()

def find_incoming_utxos(block_hash, transactions):
    """
    Iterates through all the outputs and looks for any directed to user's wallet.
    If found, save to the utxo pool
    :return:
    """
    myAddress = SHA256.new(get_public_key("string").encode()).hexdigest()

    for tnx in transactions:
        for index in range(len(tnx.outputs)):
            if tnx.outputs[index]["address"] == myAddress and len(tnx.inputs) > 0:
                save_utxo(tnx.get_transaction_id(), index, block_hash, tnx.outputs[index]["amount"])
            elif tnx.outputs[index]["address"] == myAddress and len(tnx.inputs) == 0:
                save_utxo(tnx.get_transaction_id(), -1, block_hash, tnx.outputs[index]["amount"])
