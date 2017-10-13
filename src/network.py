from src.transaction import Transaction
from flask import Flask
from flask import request
node = Flask(__name__)


@node.route('/transaction', methods=['POST'])
def send_transaction():
    if request.method == 'POST':
        data = request.get_json()
        tnx = Transaction(data)
        # if tnx.verify:
        #     # TODO: add transaction to a lit of tnxs not yet in a block
        #     return "Transaction submission successful.\n"
        # else:
        #     return "Invalid transaction.\n"


def run():
    """
    Start the flask application
    """
    node.run()
