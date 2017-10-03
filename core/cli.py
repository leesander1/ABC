from block.block import Block
from core.helpers import parse
import cmd, sys
import hashlib
import sys
import json

class CLI(cmd.Cmd, object):
    '''
    CLI class is where the controls for the CLI exist.
    '''
    prompt = 'ABC:$ '  # shows at prompt
    intro = 'Welcome to ABC - A Block Chain. Type help or ? to list commands.\n'
    conf = None  # one config file with the peers,
    wallet = {}  # wallet data
    chain = object()  # blockchain data
    peers = {}  # peers

    # --- CLI commands ---
    def do_start(self, arg):
        'Starts mining process... we might want to mine in background?'
        return

    def do_stop(self, arg):
        'Pauses mining process...'
        return

    def do_exit(self,arg):
        'Exits program'
        return

    def do_wallet(self,arg):
        'Prints address'
        return

    def do_balance(self,arg):
        'Prints balance'
        return

    def do_info(self, arg):
        'Prints the info of the node, ie block height number of peers etc'
        return

    def do_block_info(self, arg):
        'Prints the info of the block'
        return

    def do_send(self, arg):
        'Send $'
        return

    def preloop(self):
        'Do stuff on start'
        # this is where we want to check if new user
        # initialize if new user
        # 1) generate a public private key / wallet
        # 2) create genesis block and store new chain data
        # 3) make a request to generate peers
        #
        # also we want to load up any saved data if it exists
        #
        # 1) wallets / public private keys
        # 2) blockchain data
        # 3) peer data
        #
        return

    def postloop(self):
        'Do stuff on end'
        # this is where we want to save all the data on exit
        # we should also save stuff on events
        return