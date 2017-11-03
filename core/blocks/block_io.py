""" Getting and Putting blocks into json files """
import os, json

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

def save_block(b):
    # saves the block
    try:
        with open('{0}/{1}.json'.format(os.path.join(os.getcwd(), r'data'), b.block_hash()), 'w') as file:
            json.dump(b.info(), file, indent=4, sort_keys=True)
            file.close()
            pass
    except IOError as e:
        print('error saving block')