from Crypto.PublicKey import ECC
import json
import os


def generate_keys():
    """
    Generate a set of Elliptic Curve Cryptograph keys and
    store them in respective files
    """
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key()

    print(os.getcwd())
    # write private key to file
    file = open(os.path.normpath('../data/private_key.pem'), 'wt')
    file.write(private_key.export_key(format='PEM'))
    file.close()

    # write public key to file
    file = open('/../data/public_key.pem', 'wt')
    file.write(public_key.export_key(format='PEM'))
    file.close()


def write_block(block):
    """
    Append a new block to the end of the block chain
    :param block: the block object to append
    """
    file = open('..\\data\\block_chain.txt', 'a')
    file.write("{}\n".format(str(block)))


def read_block(index=-1):
    """
    Read a block from a specified block height off of the block chain.
    If no height is specified, the last block is read.
    :param index: height of block to read
    :return: the block at height `index`
    """
    file = open('.\\data\\block_chain.txt', 'r')
    # TODO: This has to read the entire file in to a list object..
    # TODO: maybe there is a better way
    return json.loads(file.readlines()[index])

