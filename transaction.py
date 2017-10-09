import json


class Transaction(object):
    def __init__(self, data=None):
        self.data = data
        self.sender = data['inputs'][0]

    def verify(self):
        return True

