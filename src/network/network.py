'''
Networking - Server
- handle seeding peers
- handle recieving new block
- handle updating chain on startup
- handle transmitting new block to network
- handle recieving new transaction from network
- handle transmitting new transaction to network
'''

from flask import Flask
from flask import request
import requests
import logging, json, os
from src.configuration import Configuration
from src.persist import block, save_verified_transaction, save_unverified_transaction
from src.core import api as core
from src.transaction import Transaction

app = Flask(__name__)
# app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def start_server():
    '''
    Starts the server and prevents default start
    :return:
    '''
    app.run(host='0.0.0.0', port='5000', use_reloader=False, debug=False)


def seed_peers():
    '''
    seed peers by connecting to firebase cloud function that returns a list of peers.
    :return:
    '''
    conf = Configuration()
    url = 'https://us-central1-abc-network.cloudfunctions.net/getpeers/'
    port = conf.get_conf("port")  # expecting {port: 50050}
    p = {'port': port}
    r = requests.get(url, params=p)  # Not currently working. maybe requires POST?
    return r.json()


def req_post(host, endpoint, port, data):
    '''
    trasmit data by making a request to peers
    :return:
    '''
    # post request
    # for each peer, make a request to the endpoint with the appropriate data
    url = 'http://{0}:{2}/{1}'.format(host, endpoint, port)
    payload = json.dumps(data)
    headers = {'content-type': 'application/json', 'dataType': 'json'}
    r = requests.post(url, data=payload, headers=headers)
    return ""

def req_get(host, endpoint, port, data=None):
    '''
    receive data from peer through a get request to an endpoint
    :return:
    '''
    # get request
    url = 'http://{0}:{2}/{1}'.format(host, endpoint, port)
    p = data
    r = requests.get(url, params=p)
    return r.json()

def transmit(data, handler):
    # send data to all peers
    conf = Configuration()
    peers = conf.get_conf("peers")
    for n in peers:
        p = peers[n]
        h = req_post(p["ip"], handler, p["port"], data)  # make post to peer

def sync():
    '''
    sync with peers by checking your height against peers and getting transactions.
    :return:
    '''
    conf = Configuration()
    peers = conf.get_conf("peers")
    for n in peers:
        p = peers[n]
        h = req_get(p["ip"], "height", p["port"])  # make request to get peers height
        while h > conf.get_conf("height"):
            nb = req_get(p["ip"], "block", p["port"], conf.get_conf("last_block"))
            core.verify_block(nb)


def verify_incoming_tnx(data):
    """
    Deserializes transaction and verifies it. If so, add it to verified transaction
    :param data: serialized transaction
    :return: None
    """
    tnx_tuple = data.items()

    tnx_payload = tnx_tuple[1]
    tnx_payload["transaction_id"] = tnx_tuple[0]

    tnx = Transaction(payload=tnx_payload)

    if tnx.verify():
        save_verified_transaction(tnx.get_transaction_id(), tnx.get_data())
    else:
        save_unverified_transaction(tnx.get_transaction_id(), tnx.get_data())

@app.route('/', methods=['GET'])
def test():
    b = block.read_block("0000fff57a5e49c38152b54edfd587c738ba33708008c995d973c2d2238179a6")
    r = transmit(b, "block")
    # r = req_post('localhost', 'block', '5001', b)
    return "working"

@app.route('/block', methods=['POST'])
# # recieve a new block from the network.
# # should verify the block
# # if valid stop mining, update height and transmit to peers
# # start mining new block
def h_block():
    # handle getting new block
    nb = request.get_json(silent=True)
    core.verify_block(json.dumps(nb))
    return json.dumps(nb)

@app.route('/block', methods=['GET'])
# # request for a certain block
# # contain params for last block hash
# # should return the next block
def r_block():
    bh = request.args.get("block")
    b = block.find_block(bh)
    return json.dumps(b)

@app.route('/height', methods=['GET'])
# request from network for block height
# should return current block height
def r_height():
    conf = Configuration()
    h = {'height': conf.get_conf("height")}
    return json.dumps(h)

@app.route('/txn', methods=['POST'])
# # recieve a new txn from the network.
# # should verify the txn
# # transmit to peers either way
# # add to verified or unverified txns list
def h_txn():
    # handle the txn
    ntxn = request.get_json(silent=True)
    verify_incoming_tnx(ntxn)
    return json.dumps(ntxn)


@app.route('/txn', methods=['GET'])
# # request for updated list of txns
# # should return list of txns
def r_txn():
    try:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'r') as file:
            data = json.load(file)
            file.close()
    except IOError:
        with open('{0}/verified_transactions.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
            data = {}
            json.dump(data, file)
            file.close()
    return json.dumps(data)

@app.route('/peers', methods=['GET'])
# request from network for peers
# should return peers
def r_peers():
    conf = Configuration()
    peers = conf.get_conf("peers")
    return json.dumps(peers)

@app.route('/ping', methods=['GET'])
# # request to check if connection is alive
# # should ping back
def ping():
    r = {'ping': 'pong'}
    return json.dumps(r)