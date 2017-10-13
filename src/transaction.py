import json


class Transaction(object):
    def __init__(self, rec_address):
        """
        Create a transaction object to an address
        :param rec_address: the receivers address (public key?)
        """
        self.rec_address = rec_address


    def get_inputs(self):
        for block in


