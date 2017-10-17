from Crypto.PublicKey import ECC
import os

# private constant file paths
_PRIVATE_KEY_PATH = os.path.normpath('../data/private_key.pem')
_PUBLIC_KEY_PATH = os.path.normpath('../data/public_key.pem')
_PRIVATE_KEY = None
_PUBLIC_KEY = None


def ensure_data_dir():
    """
    Check to see if the data directory exists.
    If not, create it
    """
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):  # check for existence
        os.mkdir(data_dir)  # create


def get_private_key():
    """
    Set the private key from a file or by creating a new one
    :return: ECC private key object
    """
    ensure_data_dir()  # ensure directory exists
    if _PRIVATE_KEY:  # if we have already retrieved the key
        key = _PRIVATE_KEY
    else:
        try:  # get existing private key
            key = ECC.import_key(open(_PRIVATE_KEY_PATH).read())
        except FileNotFoundError:  # create public key
            key = ECC.generate(curve='P-256')
            # write private key to file
            file = open(_PRIVATE_KEY_PATH, 'wt')
            file.write(key.export_key(format='PEM'))
            file.close()

    global _PRIVATE_KEY
    _PRIVATE_KEY = key  # cache the key
    return key


def get_public_key(output=None):
    """
    Get the public key from a file or by creating a new one
    :param output: can equal 'string' if the public key needs to be a string
    :return: string or ECC object representing the public key
    """
    ensure_data_dir()  # ensure directory exists
    if _PUBLIC_KEY:  # if we have already retrieved the key
        key = _PUBLIC_KEY
    else:
        private_key = get_private_key()
        try:  # get existing public key
            key = ECC.import_key(open(_PUBLIC_KEY_PATH).read())
        except FileNotFoundError:  # create public key from private key
            # write public key to file
            key = private_key.public_key() # plain text
            file = open(_PUBLIC_KEY_PATH, 'wt')
            file.write(key.export_key(format='PEM'))
            file.close()

    # return public key as string or ECC object
    global _PRIVATE_KEY
    _PRIVATE_KEY = key  # cache the key
    return key.export_key(format='OpenSSH') if output == 'string' else key


def import_public_key(public_key):
    """
    Import a plain text public key and make it into an ECC object 
    :param public_key: the public key as a string
    :return: an ECC key object
    """
    return ECC.import_key(public_key)

