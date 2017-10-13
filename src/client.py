from Crypto.PublicKey import ECC
from src.block import Block
from src.transaction import Transaction
import src.network
import json
import os

PUBLIC_KEY = None
PRIVATE_KEY = None
MY_ADDRESS = None
PRIVATE_KEY_PATH = os.path.normpath('..\\data\\private_key.pem')
PUBLIC_KEY_PATH = os.path.normpath('..\\data\\public_key.sh')
MY_ADDRESS_PATH = os.path.normpath('..\\data\\my_address.txt')
BLOCK_CHAIN_FILE_PATH = os.path.normpath('..\\data\\block_chain.txt')
UNSPENT_TRANSACTIONS_PATH = os.path.normpath('..\\data\\unspent_transactions.txt')

def get_keys():
    """
    Generate a set of Elliptic Curve Cryptograph keys and
    store them in respective files
    """


    try:  # try to load previously stored key pair

        public_key = (open(PRIVATE_KEY_PATH).read())
        private_key = ECC.import_key(open(PUBLIC_KEY_PATH).read())

    except FileNotFoundError:  # generate new key pair

        private_key = ECC.generate(curve='P-256')
        public_key = private_key.public_key().export_key(format='OpenSSH')

        # write private key to file
        # TODO: this file path is static.. if the working directory isnt src/ it wont work
        file = open(PRIVATE_KEY_PATH, 'wt')
        file.write(private_key.export_key(format='PEM'))
        file.close()

        # write public key to file
        # TODO: this file path is static.. if the working directory isnt src/ it wont work
        file = open(PUBLIC_KEY_PATH, 'wt')
        file.write(public_key)
        file.close()

    global PUBLIC_KEY  # assign the public key globally
    PUBLIC_KEY = public_key
    global PRIVATE_KEY  # assign the private key globally
    PRIVATE_KEY = private_key


def get_address():
    """
    Get this nodes address from a file. If the file does not exist,
    create it and write an address.
    :return: 
    """
    try:
        file = open(MY_ADDRESS_PATH, 'r')
        address = file.read()
        file.close()
    except FileNotFoundError:
        file = open(MY_ADDRESS_PATH, 'wt')
        address = 'dane'
        file.write(address)
        file.close()

    global MY_ADDRESS
    MY_ADDRESS = address


def write_block(block):
    """
    Append a new block to the end of the block chain
    :param block: the block object to append
    """
    # TODO: this file path is static.. if the working directory isnt src/ it wont work
    file = open(BLOCK_CHAIN_FILE_PATH, 'a')
    file.write("{}\n".format(block))
    file.close()


def read_block_chain(index=None):
    """
    Read a block from a specified block height off of the block chain.
    If no height is specified, the last block is read.
    :param index: height of block to read
    :return: the block at height `index`
    """
    # TODO: this file path is static.. if the working directory isnt src/ it wont work
    file = open(BLOCK_CHAIN_FILE_PATH, 'r')
    # TODO: This has to read the entire file in to a list object..
    # TODO: maybe there is a better way
    if index:
        blocks = [Block(**json.loads(x)) for x in file.readlines()[index]]
    else:
        blocks = [Block(**json.loads(x)) for x in file.readlines()]
    file.close()
    return blocks


def write_my_transactions(block):
    """
    Save all transactions in a block where MY_ADDRESS appears in the 
    receiving position of any of the outputs
    :param block: a Block object
    """
    file = open(UNSPENT_TRANSACTIONS_PATH, 'a')

    for i, transaction in block.get_transactions().items() :
        tnx = Transaction(**transaction)  # convert to Transaction object
        for output in tnx.get_outputs():
            if output[1] == MY_ADDRESS:  # receiver is position 1 of output
                file.write("{}\n".format(tnx))

    file.close()


def overwrite_my_transactions(transactions):
    """
    Overwrite all contents in the my unspent transactions file
    :param transactions: 
    :return: 
    """
    file = open(UNSPENT_TRANSACTIONS_PATH, 'wt')
    for tnx in transactions:
        file.write("{}\n".format(tnx))
    file.close()


def read_my_transactions():
    """
    Read in all saved transactions addressed to this node
    :return: a list of transactions
    """
    try:
        file = open(UNSPENT_TRANSACTIONS_PATH, 'r')
        transactions = [Transaction(**json.loads(x)) for x in file.readlines()]
        file.close()
    except FileNotFoundError:  # no transactions file found
        transactions = []
    return transactions


def create_transaction(rec_address, amount):
    """
    Create a transaction (gather inputs, outputs, and 
    format them into a Transaction object and then sign the transaction.
    :param rec_address: the address of the receiver
    :param amount: the amount to the receivers address
    :return: a complete filled out Transacttion object
    """
    inputs = []
    outputs = []
    total = 0

    # get inputs
    unspent_transactions = read_my_transactions()
    for tnx in unspent_transactions:
        for output in tnx.get_outputs():  # for each output
            if total < amount and output[1] == MY_ADDRESS:
                inputs.append(output)  # add this output as an input
                unspent_transactions.remove(tnx)
                total += output[2]  # add outputs value to total

    # update unspent transactions
    overwrite_my_transactions(unspent_transactions)

    # create outputs
    outputs.append((rec_address, MY_ADDRESS, amount))
    total -= amount
    if total != 0:
        outputs.append((MY_ADDRESS, MY_ADDRESS, total))

    # build the transaction object
    transaction = Transaction(sender_pubkey=PUBLIC_KEY)
    transaction.set_message(inputs, outputs)
    transaction.generate_id()
    transaction.sign(PRIVATE_KEY)
    return transaction

def send_transaction(rec_address, amount):
    """
    Send a transaction over the network.
    :param rec_address: the address of the receiver
    :param amount: the amount to the receivers address
    """
    tnx = create_transaction(rec_address, amount)
    print("Sending Transaction: {}".format(tnx))
    return tnx

def create_genesis():
    """
    Create a genesis block (the first block in the block chain)
    :return: 
    """
    data = {  # one transaction
        0:  {
                "id": "",  # TODO: hash of message
                "signature": "need_signature",  # TODO: one time key pair for genesis tnx
                "sender_pubkey": "need_public",  # TODO: one time key pair for genesis
                "message": {
                    "inputs": [
                        ("null", "genesis", 7000),
                        ("null", "genesis", 7000),
                        ("null", "genesis", 7000),

                    ],
                    "outputs": [
                        ("genesis", "kevin", 7000),
                        ("genesis", "dane", 7000),
                        ("genesis", "lee", 7000),
                    ]
                }
            }
    }
    return Block(index=0, data=data, previous_hash="0")