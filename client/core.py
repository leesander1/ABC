""" core functionality """
from block.block import Block, genesis_block
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
        conf = increment_height(conf)

    return conf

def load_conf():
    # loads the config file
    try:
        with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data'))) as file:
            # read in the data
            data = json.load(file)
            file.close()
            pass
    except IOError as e:
        # file does not exist or not able to read file
        data = create_conf()
        print("not able to open conf file")
    return data

def create_conf():
    # creates a new config
    conf = {
        'height': 0,
        'last_block': "0000b7efc7281627c3a296475b8e142e8a280ea34c22718e6fb16d8aa7a9423e",
        'version': "00000001",
        'difficulty': 4,
        'reward': 100,
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
        with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
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
        with open('{0}/abc.json'.format(os.path.join(os.getcwd(), r'data')), 'w') as file:
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

def increment_height(conf):
    # updates the height of the chain in the conf
    conf["height"] += 1
    updated = save_conf(conf)
    return updated

def update_previous_hash(conf, block_hash):
    # updates the height of the chain in the conf
    conf["last_block"] = block_hash
    updated = save_conf(conf)
    return updated

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

def bundle_tnx(cbtx):
    """
    pull some verified transactions
    :return: tnx
    """
    # tnx = [cbtx, 'test7', 'test8', 'test9', 'test10']  # need to actually get real tnxs
    tnx = ['test6', 'test7', 'test8', 'test9', 'test10', 'test11']  # need to actually get real tnxs
    return tnx

def mine(conf):
    # Mines blocks
    reward_address = conf["wallet"]["address"]
    reward_amount = conf["reward"]
    # 1) add coinbase tx with reward
    cbtx = {reward_address, reward_amount}

    # 2) bundle transactions
    tnx = bundle_tnx(cbtx)

    b = Block(previous_hash=conf["last_block"], transactions=tnx)
    Block.target(b, conf["difficulty"])
    Block.mine(b)
    save_block(b)
    increment_height(conf)
    update_previous_hash(conf, b.block_hash())
    # 3) if success, save block, update db, update config with updated previous_hash & height
    # 4) notify network
    # 5) repeat
    return