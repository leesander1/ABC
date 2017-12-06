""" Getting and Putting blocks into json files """
import json
import os
from src.persist.utxo import save_utxo
from src.configuration import Configuration


def read_block(block_hash):
    # loads the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), block_hash)) as file:
            # read in the data
            data = json.load(file)
            file.close()
    except IOError as e:
        # file does not exist or not able to read file
        data = {}
        print(e)

    return data


def find_block(parent_hash=None, block_hash=None):
    # find the next block based on hash..
    if not block_hash:
        conf = Configuration()
        block_hash = conf.get_conf("last_block")

    b = read_block(block_hash)
    if b["header"]["parent"] == parent_hash:
        return b
    else:
        find_block(parent_hash, b["header"]["parent"])


def save_block(b):
    # saves the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), b.block_hash()), 'w') as file:
            json.dump(b.info(), file, indent=4, sort_keys=True)
            file.close()
    except IOError as e:
        print(e)