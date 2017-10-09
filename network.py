from client import my_transactions
from transaction import Transaction
from flask import Flask
from flask import request
node = Flask(__name__)

@node.route('/create_tnx', methods=['POST'])
def create_transaction():
    if request.method == 'POST':
        data = request.get_json()
        tnx = Transaction(data)
        if tnx.verify:
            my_transactions.append(tnx)
            return "Transaction submission successful.\n"
        else:
            return "Invalid transaction.\n"


node.run()