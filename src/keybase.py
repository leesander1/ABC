from Crypto.PublicKey import ECC
import os


class AbcKey(object):

    _PRIVATE_KEY_PATH = os.path.normpath('../data/private_key.pem')
    _PUBLIC_KEY_PATH = os.path.normpath('../data/public_key.pem')

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.private_key = self.set_private_key()
        self.public_key = self.set_public_key()

    def set_private_key(self):
        """
        Set the private key from a file or by creating a new one
        :return: ECC private key object
        """
        try:  # get existing private key
            private_key = ECC.import_key(open(self._PRIVATE_KEY_PATH).read())
        except FileNotFoundError:  # create public key
            private_key = ECC.generate(curve='P-256')
            # write private key to file
            file = open(self._PRIVATE_KEY_PATH, 'wt')
            file.write(private_key.export_key(format='PEM'))
            file.close()
        return private_key

    def set_public_key(self):
        """
        Set the public key from a file or by creating a new one
        :return: ECC public key object
        """
        if not self.private_key:  # private key must be set first
            self.private_key = self.set_private_key()

        try:  # get existing public key
            public_key = ECC.import_key(open(self._PUBLIC_KEY_PATH).read())
        except FileNotFoundError:  # create public key from private key
            # write public key to file
            public_key = self.private_key.public_key() # plain text
            file = open(self._PUBLIC_KEY_PATH, 'wt')
            file.write(public_key.export_key(format='PEM'))
            file.close()
        return public_key

    def get_private(self):
        """
        Get the private ECC key object
        :return: ECC private key object
        """
        return self.private_key

    def get_public(self):
        """
        Get the public ECC key as a plaintext string
        :return: the public key as a string
        """
        return self.public_key.export_key(format='OpenSSH')


def import_key(public_key):
    """
    Import a plain text public key and make it into an ECC object 
    :param public_key: the public key as a string
    :return: an ECC key object
    """
    return ECC.import_key(public_key)



