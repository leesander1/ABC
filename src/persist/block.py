""" Getting and Putting blocks into json files """
import json
import os
from src.transaction import Transaction
from src.persist.utxo import save_utxo


def read_block(block_hash):
    # loads the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), block_hash)) as file:
            # read in the data
            data = json.load(file)
            file.close()
            return data
    except IOError as e:
        # file does not exist or not able to read file
        print('{0}'.format(e))

def save_block(b):
    # saves the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), b.block_hash()), 'w') as file:
            json.dump(b.info(), file, indent=4, sort_keys=True)
            file.close()

        # TODO: A func will be written to add utxos to user when verifying block. This part will be deprecated then.
        info = b.info()
        header = info["header"]

        tnx_tuple = info["transactions"].popitem()
        tnx_payload = {"transaction_id": tnx_tuple[0]}
        tnx_payload.update(tnx_tuple[1])
        tnx = Transaction(payload=tnx_payload)

        # genesis block
        if header["parent"] == "0000000000000000000000000000000000000000000000000000000000000000":
            save_utxo(tnx.get_transaction_id(), -1, info["block"], 7000)

    except IOError as e:
        print('error saving block')