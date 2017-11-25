import copy
import json
import os

_PATH_UNSPENT_TNX = '{0}/utxo.json'.format(os.path.join(os.getcwd(), r'data'))


def get_unspent_outputs(amount):
    """
    Create a dict of unspent transaction outputs that add up
    to or exceed `amount`
    NOTE: This function assumes that the TX fee is included in the param amount
    NOTE: This is most efficient if UTXOs are sorted in descending amount value
    :param amount: the minimum amount required from the utxos
    :return: a dict of utxo's if sufficient funds found, otherwise an empty dict. Also returns utxo sum
    """

    try:
        with open(_PATH_UNSPENT_TNX) as file:
            data = json.load(file)
            file.close()
    except IOError:
        with open(_PATH_UNSPENT_TNX, 'w') as file:
            data = {}
            json.dump(data, file)
            file.close()

    utxos = copy.deepcopy(data)
    selected_utxos = []
    utxo_sum = 0

    # NOTE: This is random at the moment
    for key, value in utxos.items():
        if utxo_sum < amount:
            selected_utxos.append({
                "transaction_id": key,
                "output_index": value["index"],
                "block_hash": value["block"]})
            data.pop(key)
            utxo_sum = utxo_sum + value["amount"]
        else:
            break

    if utxo_sum >= amount:
        # if there was sufficient funds, remove them from the utxo file
        with open('{0}/utxo.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            json.dump(data, file)
            file.close()
    else:
        raise ValueError("Insufficient funds")
    return selected_utxos, utxo_sum


def find_unspent_output(transaction_id, output_index, block_hash):
    """
    Get an unspent transaction output from the block chain
    :param transaction_id: id of the transaction
    :param output_index: index of the output within the transaction
    :param block_hash: the block hash of the transaction
    :return:

        a dict representing an unspent transaction output in the form:

        {
            "transaction_id": "",
            "output_index": "",
            "address": "",
            "amount": ""
        }

    """

    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), block_hash)) as file:
            data = json.load(file)
            file.close()

            output = data["transactions"][transaction_id]["outputs"][output_index]

            # adding additional info to the output object(since the output structure does not include index or id)
            output["transaction_id"] = transaction_id
            output["output_index"] = output_index

        return output
    except IOError as e:
        # file does not exist or not able to read file
        print(e)
    except KeyError as e:
        # error finding utxo
        print('Transaction not found\nTXID:{0}'.format(e))

def save_utxo(transaction_id, output_index, block_hash, amount):
    new_utxo = {"{0}".format(transaction_id): {
        "amount": amount,
        "index": output_index,
        "block": block_hash
    }}

    try:
        with open(_PATH_UNSPENT_TNX, 'r+') as file:
            data = json.load(file)

            data.update(new_utxo)
            json.dump(data, file)
            file.close()
    except IOError:
        with open(_PATH_UNSPENT_TNX, 'w') as file:
            data = {}

            data.update(new_utxo)
            json.dump(data, file)
            file.close()

