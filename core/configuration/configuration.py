""" Singleton used to access client config """
import os, json

from Crypto.Hash import SHA256

from core.configuration.singleton import Singleton
from core.blocks.block_io import save_block, read_block
from core.blocks.block import Block, genesis_block
from core.wallet.wallet import get_private_key, get_public_key

class Configuration(metaclass=Singleton):
    def __init__(self):
        """
        1) check to see if conf appdata exists
        2) if it does load it up then begin sync ( connect, get updates, etc )
        3) if not, create new public key/wallet, files, mine genesis block, connect to some seed peers, sync
        """
        self.conf = self.load_conf()
        if self.conf["height"] == 0:
            # we need to save the genesis block
            b = genesis_block()
            # create a new folder dir for blocks
            cwd = os.getcwd()
            try:
                os.makedirs(os.path.join(cwd, r'data'))
            except OSError as e:
                # folder exists or error
                # print('error {0}'.format(e))
                pass
            save_block(b)
            self.increment_height()

    def load_conf(self):
        # loads the config file
        try:
            with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data'))) as file:
                # read in the data
                data = json.load(file)
                file.close()
                pass
        except IOError as e:
            # file does not exist or not able to read file
            data = self.create_conf()
            print("not able to open conf file")
        return data

    def create_conf(self):
        # creates a new config
        pubkey = get_public_key("string")
        hashed_address = SHA256.new(pubkey.encode()).hexdigest()

        conf = {
            'height': 0,
            'last_block': "0000b7efc7281627c3a296475b8e142e8a280ea34c22718e6fb16d8aa7a9423e",
            'version': "00000001",
            'difficulty': 4,
            'reward': 100,
            'wallet': {
                'address': hashed_address,
                'amount': 0
            },
            'peers': {
                '1': {
                    'ip': "127.0.0.1",
                    'port': 3390
                },
                '2': {
                    'ip': "localhost",
                    'port': 3390
                }
            }
        }
        # call save_conf
        obj = json.dumps(conf)
        parsed = json.loads(obj)
        try:
            with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
                json.dump(parsed, file, indent=4, sort_keys=True)
                file.close()
                pass
        except IOError as e:
            print('error creating conf')
        return parsed

    def save_conf(self):
        try:
            with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
                json.dump(self.conf, file, indent=4, sort_keys=True)
                file.close()
                pass
        except IOError as e:
            print('error saving conf')

    def increment_height(self):
        # updates the height of the chain in the conf
        self.conf["height"] += 1
        self.save_conf()

    def update_previous_hash(self, block_hash):
        # updates the height of the chain in the conf
        self.conf["last_block"] = block_hash
        self.save_conf()
        return self.conf

    def get_conf(self, key=None):
        """
        returns the value for the matching key in the configuration
        :param key: key
        :return: value for the key
        """
        try:
            if key:
                return self.conf.get(key)
            else:
                return self.conf
        except KeyError as e:
            print("Key was not found: {0}".format(e))
