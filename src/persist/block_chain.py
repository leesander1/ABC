import json
import os

# private constant file paths
_PATH_BLOCK_CHAIN = os.path.normpath('../data/block_chain.txt')
_PATH_UNSPENT_TNX = os.path.normpath('../data/utxos.txt')


def ensure_data_dir():
    """
    Check to see if the data directory exists.
    If not, create it
    """
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):  # check for existence
        os.mkdir(data_dir)  # create


def write_block(block):
    """
    Write a new Block object to the block chain file in JSON format
    :param block: the Block object
    :return: True if successful write, false otherwise
    """
    ensure_data_dir()  # ensure data directory exists
    success = False

    if block.index == 0:  # genesis block
        file = open(_PATH_BLOCK_CHAIN, 'wt')
        data = block.get_data()
        dump = json.dumps(data)
        file.write("{}\n".format(dump))
        file.close()
        success = True
    else:  # not genesis block
        prev_block = read_all_blocks()[-1]  # get the last block
        if prev_block['hash'] == block.get_previous_hash()\
                and block.index - 1 == prev_block['index']:  # validate block
            file = open(_PATH_BLOCK_CHAIN, 'a')  # append to block chain
            file.write("{}\n".format(json.dumps(block.get_data())))
            file.close()
            success = True
    return success


def read_all_blocks():
    """
    Read all blocks from the block chain file
    :return: a list of Block objects
    """
    ensure_data_dir()  # ensure data directory exists
    try:
        block_list = open(_PATH_BLOCK_CHAIN, 'r').readlines()
        # convert each json object to a Block object
        block_list = [json.loads(block) for block in block_list]
    except FileNotFoundError as e:
        block_list = []
    return block_list


def write_unspent_outputs(block, public_key):
    """
    Write all unspent transaction outputs from a newly mined block
    that belong to the address at `public_key` into this node's
    unspent output file for later use.
    :param block: the newly mined block
    :param public_key: full public key of this node
    :return: 
    """