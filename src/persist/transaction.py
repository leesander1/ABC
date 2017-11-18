import os, json

def save_verified_transaction(tnx_id, tnx_data):
    """
    Saves the transaction to the verified pool.
    Note that it will save the transaction as a key-value pair where the id is the key and the rest is the value
    :param tnx_id: transaction id
    :param tnx_data: transaction data
    :return: None
    """
    verified_tnx = {tnx_id: tnx_data}
    try:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r+') as file:
            data = json.load(file)
            data.update(verified_tnx)
            json.dump(data, file)
            file.close()
    except IOError as e:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            data.update(verified_tnx)
            json.dump(data, file)
            file.close()

def save_unverified_transaction(tnx_id, tnx_data):
    """
    Saves the transaction to the unverified pool.
    Note that it will save the transaction as a key-value pair where the id is the key and the rest is the value
    :param tnx_id: transaction id
    :param tnx_data: transaction data
    :return: None
    """
    unverified_tnx = {tnx_id: tnx_data}
    try:
        with open('{0}/unverified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r+') as file:
            data = json.load(file)
            data.update([unverified_tnx])
            json.dump(data, file)
            file.close()
    except IOError as e:
        with open('{0}/unverified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            data.update([unverified_tnx])
            json.dump(data, file)
            file.close()