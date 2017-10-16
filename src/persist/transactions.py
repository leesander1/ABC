from src.transaction import Transaction
import json
import os

_PATH_UNSPENT_TNX = os.path.normpath('../data/received_transactions.txt')


def ensure_data_dir():
    data_dir = os.path.normpath('../data/')
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def write_transaction(transactions):
    ensure_data_dir()
    pass


def read_all_transactions():
    ensure_data_dir()
    pass
