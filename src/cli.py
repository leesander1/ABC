''' The cmd line interface '''

import cmd
from src import client


class CLI(cmd.Cmd, object):
    """
    CLI class is where the controls for the CLI exist.
    """

    prompt = 'ABC:$ '  # shows at prompt
    intro = 'Welcome to ABC - A Block Chain. Type help or ? to list commands.\n'
    conf = None  # one config file with the peers,
    wallet = {}  # wallet data
    peers = {}  # peers

    def do_send(self, arg):
        args = arg.split()
        tx = client.send_transaction(args[0], int(args[1]))

    def onecmd(self, line):
        """
        define $ as a shortcut for the mine command. x for exit
        and ask for confirmation when the interpreter exit
        :return: returns a response r
        """
        if line[:1] == '$':
            line = 'start '+line[1:]
        elif line[:1] == 'x':
            line = 'exit ' + line[1:]
        r = super(CLI, self).onecmd(line)
        if r:
            r = input('Are you sure you want to exit?(y/n):')=='y'
        return r

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
        client.create_genesis()
        return

    def postloop(self):
        'Do stuff on end'
        # this is where we want to save all the data on exit
        # we should also save stuff on events

        return