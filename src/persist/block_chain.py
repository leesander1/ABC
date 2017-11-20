import json
import os
from Crypto.Hash import SHA256

# private constant file paths
_PATH_BLOCK_CHAIN = os.path.normpath('../data/block_chain.txt')
_PATH_UNSPENT_TNX = os.path.normpath('../data/utxos.txt')

#
# def ensure_data_dir():
#     """
#     Check to see if the data directory exists.
#     If not, create it
#     """
#     data_dir = os.path.normpath('../data/')
#     if not os.path.isdir(data_dir):  # check for existence
#         os.mkdir(data_dir)  # create


def write_block(block):
    """
    Write a new (non-genesis) block to the block chain file.
    :param block: the block to write
    :return: 
    """
    try:
        file = open(_PATH_BLOCK_CHAIN, 'r+')
        block_chain = json.load(file)
        block_chain['blocks'].append(block.get_data())
        file.seek(0)
        file.truncate()
        json.dump(block_chain, file, sort_keys=True, indent=4)
        file.close()
    except FileNotFoundError as e:
        print(e)


def write_genesis_block(block):
    """
    Write the genesis block to the block chain file.
    :param block: 
    :return: 
    """
    try:
        file = open(_PATH_BLOCK_CHAIN, 'w')
        block_chain = {'blocks': [block.get_data()]}
        json.dump(block_chain, file, sort_keys=True, indent=4)
        file.close()
    except FileNotFoundError as e:
        print(e)


def read_all_blocks():
    """
    Read all blocks from the block chain file
    :return: a list of Block objects
    """
    try:
        file = open(_PATH_BLOCK_CHAIN, 'r')
        blocks = json.load(file)['blocks']
    except FileNotFoundError as e:
        print(e)
        blocks = []
    return blocks


def write_unspent_outputs(block, public_key):
    """
    Write all unspent transaction outputs from a newly mined block
    that belong to the address at `public_key` into this node's
    unspent output file for later use.
    :param block: the newly mined block
    :param public_key: full public key of this node
    :return: 
    """
    my_address = SHA256.new(public_key.encode('utf-8')).hexdigest()
    try:
        file = open(_PATH_UNSPENT_TNX, 'a')
        # go through each transaction and see if it is addressed
        # to this node, adding it to the file if so
        for tnx in block.get_transactions():
            for idx in range(0, len(tnx['outputs'])):
                output = tnx['outputs'][idx]
                if output['address'] == my_address:
                    unspent_output = json.dumps({
                        "transaction_id": tnx['transaction_id'],
                        "output_index": idx,
                        "amount": output['amount']
                    })
                    file.write("{}\n".format(unspent_output))
    except FileNotFoundError as e:
        print(e)


def find_unspent_output(transaction_id, output_index):
    """
    Find an unspent transaction output in the block chain (for verifying
    transactions) 
    :param transaction_id: the id of the transaction containing the output
    :param output_index: the index of the output in the transaction
    :return: 
    """

    try:
        file = open(_PATH_BLOCK_CHAIN, 'r')
        block_chain = json.load(file)
        file.close()
        output = {}
        for block in block_chain['blocks']:
            for transaction in block['transactions']:
                if transaction['transaction_id'] == transaction_id:
                    output = transaction['outputs'][output_index]
                    break
    except (FileNotFoundError, IndexError) as e:
        output = {}
        print(e)

    return output


def get_my_balance():
    """
    Get the total amount of unspent transaction outputs for this
    node.
    :return: int of balance
    """
    try:
        file = open(_PATH_UNSPENT_TNX, 'r')
        transactions = [json.loads(x) for x in file.readlines()]
        file.close()
        balance = sum([int(tnx['amount']) for tnx in transactions])
    except FileNotFoundError as e:
        balance = None
        print(e)
    return balance


def get_unspent_outputs(required_amount):
    """
    Gather unspent transaction outputs from this node's file for fulfilling
    new transaction inputs
    :param required_amount: minimum amount for the sum of the unspent outputs
    :return: a dict of unspent outputs and their total amount
    """
    total = 0
    using = []
    try:
        file = open(_PATH_UNSPENT_TNX, 'r')
        transactions = [json.loads(x) for x in file.readlines()]
        file.close()
        for transaction in transactions:
            total += int(transaction.pop('amount'))
            using.append(transaction)
            if total >= required_amount:
                break

        if total >= required_amount:
            left = [x for x in transactions
                    if x['transaction_id'] not in
                    [y['transaction_id'] for y in using]]
            file = open(_PATH_UNSPENT_TNX, 'w')
            for tnx in left:
                file.write("{}\n".format(json.dumps(tnx)))
            file.close()
        else:
            raise ValueError("Insufficient Funds")
    except FileNotFoundError as e:
        print(e)
    return using, total
