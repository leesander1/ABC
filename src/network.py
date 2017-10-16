from src.transaction import Transaction
from flask import Flask
from flask import request
node = Flask(__name__)


@node.route('/transaction', methods=['POST'])
def receive_transaction():
    """
    Receive a new transaction from a node on the network
    :return:  transaction success message
    """
    if request.method == 'POST':
        data = request.get_json()
        tnx = Transaction(payload=data)
        if tnx.verify:
            # TODO: add transaction to a lit of not yet in a block
            return "Transaction submission successful.\n"
        else:
            return "Invalid transaction.\n"


def run():
    """
    Start the flask application
    """
    node.run()
