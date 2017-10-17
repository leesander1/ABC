from src.block import Block
import json
import os

_PATH_BLOCK_CHAIN = os.path.normpath('../data/block_chain.txt')


def ensure_data_dir():
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def write_block(block):
    """
    Write a new Block object to the block chain file in JSON format
    :param block: the Block object
    :return: True if successful write, false otherwise
    """
    ensure_data_dir()
    success = False
    if block.index == 0:  # genesis block
        file = open(_PATH_BLOCK_CHAIN, 'wt')
        file.write("{}\n".format(json.dumps(block.get_data())))
        file.close()
        success = True
    else:  # not genesis block
        all_blocks = read_all_blocks()
        if all_blocks:
            prev_block = all_blocks[-1]
            if prev_block.get_hash() == block.get_previous_hash()\
                    and block.index - 1 == prev_block.index:
                file = open(_PATH_BLOCK_CHAIN, 'a')
                file.write("{}\n".format(json.dumps(block.get_data())))
                file.close()
                success = True

    return success


def read_all_blocks():
    """
    Read all blocks from the block chain file
    :return: a list of Block objects
    """
    ensure_data_dir()
    try:
        block_list = open(_PATH_BLOCK_CHAIN, 'r').readlines()
        block_list = [Block(payload=json.loads(block)) for block in block_list]
    except FileNotFoundError as e:
        block_list = []
    return block_list
