import json
import os
from Crypto.Hash import SHA256
from persist.abc_key import get_public_key


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
    Wrte a block object to the block chain file in json format
    :param block: the Block object
    :return: the json representation of the block
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
            dump = json.dumps(block.get_data())
            file.write("{}\n".format(dump))
            file.close()
            success = True

    if success:
        write_unspent_outputs(block, get_public_key())
    return success


def read_all_blocks():
    """
    Read all blocks from the block chain file
    :return: a list of Block objects
    """
    ensure_data_dir()  # ensure data directory exists
    try:
        file = open(_PATH_BLOCK_CHAIN, 'r')
        block_list = [json.loads(block) for block in file.readlines()]
        file.close()
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
    file = open(_PATH_UNSPENT_TNX, 'a')
    hashed_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
    for tnx in block.get_transactions():
        for i in range(0, len(tnx['outputs'])):
            output = tnx['outputs'][i]
            address = output['address']
            if address == hashed_address:
                utxo = {"transaction_id": tnx['transaction_id'],
                        "output_index": i,
                        "amount": output['amount']}
                file.write("{}\n".format(json.dumps(utxo)))

    file.close()


def find_unspent_output(transaction_id, output_index):
    """
    Find an unspent transaction output in either the block chain (for verifying
    transactions) or in the node's unspent transaction outputs file (for 
    creating new transactions)
    :param transaction_id: the id of the transaction containing the output
    :param output_index: the index of the output in the transaction
    :param use_block_chain: Search the block chain or not
    :return: 
    """
    ensure_data_dir()
    file = open(_PATH_BLOCK_CHAIN, 'r')
    block_chain = [json.loads(x) for x in file.readlines()]
    file.close()
    output = {}
    i = 0
    while i < len(block_chain) and not output:
        j = 0
        transactions = block_chain[i]['data']
        while j < len(transactions):
            transaction = transactions[j]
            if transaction['transaction_id'] == transaction_id:
                output = transaction['outputs'][output_index]
                break
            j += 1
        i += 1

    return output


def get_unspent_outputs(required_amount):
    """
    Gather unspent transaction outputs from this node's file for fulfilling
    new transaction inputs
    :param required_amount: minimum amount for the sum of the unspent outputs
    :return: a dict of unspent outputs and their total amount
    """
    ensure_data_dir()

    file = open(_PATH_UNSPENT_TNX, 'r')
    json_transactions_list = [json.loads(x) for x in file.readlines()]
    file.close()

    total = 0
    payload = []
    i = 0
    # Iterate through each item until we have enough
    while i < len(json_transactions_list) and total < required_amount:
        transaction = json_transactions_list[i]
        tnx_id = transaction['transaction_id']
        output_index = transaction['output_index']
        amount = transaction['amount']
        total += int(amount)
        payload.append({"transaction_id": tnx_id, "output_index": output_index})
        del json_transactions_list[i]

    file = open(_PATH_UNSPENT_TNX, 'w')
    # re-write remaining transactions
    for tnx in json_transactions_list:
        file.write("{}\n".format(tnx))
    file.close()

    return payload, total
