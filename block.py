import hashlib as hasher
import datetime as date
import json


class Block(object):
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        payload = str(self.index) + \
                  str(self.timestamp) + \
                  str(self.data) + \
                  str(self.previous_hash)

        sha.update(payload.encode('utf-8'))

        return sha.hexdigest()

    def get_transactions(self):
        return self.data

    def get_next_block(self):
        new_idx = self.index + 1
        new_timestamp = date.datetime.now()
        new_data = ""  # TODO: needs data
        new_hash = self.hash
        return Block(new_idx, new_timestamp, new_data, new_hash)

    @staticmethod
    def create_genesis():
        # TODO: needs data
        data = json.dumps({
            "inputs": [
                ("null", "genesis", 7000),
                ("null", "genesis", 7000),
                ("null", "genesis", 7000),

            ],
            "outputs": [
                ("genesis", "kevin", 7000),
                ("genesis", "dane", 7000),
                ("genesis", "lee", 7000),
            ]
        })
        return Block(0, date.datetime.now(), data, "0")
