''' core functionality '''
from block.block import Block, genesis_block
from client.helpers import parse
import cmd, sys, hashlib, json, os, codecs

def initialize():
    # initialize program on startup
    # 1) check to see if conf appdata exists
    # 2) if it does load it up then begin sync ( connect, get updates, etc )
    # 3) if not, create new public key/wallet, files, mine genesis block, connect to some seed peers, sync
    conf = load_conf()
    if conf["height"] == 0:
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
        conf["height"] = 1
    # print(json.dumps(conf, indent=4, sort_keys=True))
    return conf

def load_conf():
    # loads the config file
    try:
        with open('abc.json') as file:
            # read in the data
            data = json.load(file)
            file.close()
            pass
    except IOError as e:
        # file does not exist or not able to read file
        data = create_conf()
        # print("not able to open conf file")
    return data

def create_conf():
    # creates a new config
    conf = {
        'height': 0,
        'last_block': "0000669a5bd0d672a499608a45c24649584fb0b40c8ef6a5f9e6765caf5ae892",
        'version': "00000001",
        'difficulty': 4,
        'key': {
            'private': "private_key",
            'public': "public_key",
        },
        'wallet': {
            'address': "my_address",
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
    obj = json.dumps(conf)
    parsed = json.loads(obj)
    try:
        with open('abc.json', 'w') as file:
            json.dump(parsed, file, indent=4, sort_keys=True)
            file.close()
            pass
    except IOError as e:
        print('error creating conf')
    return parsed

def save_conf(conf):
    obj = json.dumps(conf)
    parsed = json.loads(obj)
    try:
        with open('abc.json', 'w') as file:
            json.dump(parsed, file, indent=4, sort_keys=True)
            file.close()
            pass
    except IOError as e:
        print('error saving conf')
    return parsed

def save_block(b):
    # saves the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), b.block_hash()), 'w') as file:
            json.dump(b.info(), file, indent=4, sort_keys=True)
            file.close()
            pass
    except IOError as e:
        print('error saving block')
    return

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
