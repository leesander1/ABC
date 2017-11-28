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
from src.configuration import Configuration

app = Flask(__name__)
# app.logger.disabled = True


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


# def trasmit():
#     '''
#     trasmit data by making a request to peers
#     :return:
#     '''
#     # post request
#     # for each peer, make a request to the endpoint with the appropriate data
#     url = 'http://{0}:{2}/{1}'.format(host, endpoint, port)
#     payload = data
#     headers = {'content-type': 'application/json'}
#     r = requests.post(url, data=payload, headers=headers)
#     return r.json()
#
# def recieve():
#     '''
#     receive data from peer through a get request to an endpoint
#     :return:
#     '''
#     # get request
#     url = 'http://{0}:{2}/{1}'.format(host, endpoint, port)
#     p = data
#     r = requests.get(url, params=p)
#     return r.json()

@app.route('/', methods=['GET'])
def test():
    print("working.")
    data = seed_peers()

# @app.route('/block', methods=['POST'])
# # recieve a new block from the network.
# # should verify the block
# # if valid stop mining, update height and transmit to peers
# # start mining new block
#
# @app.route('/block', methods=['GET'])
# # request for a certain block
# # contain params for last block hash
# # should return the next block
#
# @app.route('/height', methods=['GET'])
# # request from network for block height
# # should return current block height
#
# @app.route('/txn', methods=['POST'])
# # recieve a new txn from the network.
# # should verify the txn
# # transmit to peers either way
# # add to verified or unverified txns list
#
# @app.route('/txn', methods=['GET'])
# # request for updated list of txns
# # should return list of txns
#
# @app.route('/peers', methods=['GET'])
# # request from network for peers
# # should return peers
#
# @app.route('/ping', methods=['GET'])
# # request to check if connection is alive
# # should ping back
