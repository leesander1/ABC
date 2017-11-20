""" Singleton used to access client config """
import json
import os

from Crypto.Hash import SHA256
from src.wallet import get_public_key

# private path
_CONFIGURATION_PATH = os.path.normpath('../data/abc.json')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(metaclass=Singleton):
    def __init__(self):
        """
        1) check to see if conf appdata exists
        2) if it does load it up then begin sync ( connect, get updates, etc )
        3) if not, create new public key/wallet, files, connect to some seed peers, sync
        """
        self.conf = {}
        self.load_conf()

    def load_conf(self):
        # loads the config file
        try:
            with open(_CONFIGURATION_PATH) as file:
                # read in the data
                self.conf = json.load(file)
                file.close()
                pass
        except IOError as e:
            # file does not exist or not able to read file
            self.create_conf()
            print("Creating new configuration")

    def create_conf(self):
        # creates a new config
        pubkey = get_public_key("string")
        hashed_address = SHA256.new(pubkey.encode()).hexdigest()

        self.conf = {
            'height': 0,
            'last_block': "0000fefed401235a109a448231ab71ff708b94270be94a855bd51220a94ad940",
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
        self.save_conf()

    def save_conf(self):
        try:
            with open(_CONFIGURATION_PATH, 'w') as file:
                json.dump(self.conf, file, indent=4, sort_keys=True)
                file.close()
        except IOError as e:
            print('{0}'.format(e))

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
