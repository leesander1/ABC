import client
from block import Block
from persist import block_chain

from src.cli import CLI
# TODO: Check the status of the network, respond accordingly
# TODO: wait for command from user

cli = CLI()
cli.cmdloop()
#####################################################################
#
#
#       TESTING BELOW
#
#
#####################################################################

# # Create genesis
# print("Creating Genesis Block")
# g_block = client.create_genesis()
#
#
#
# # create new transaction and "send" it
# print("Sending transaction to address1 for 400 ABC")
# tnx = client.create_transaction("address1", 400)
# client.send_transaction(tnx)
#
#
# # create a new block
# print("CREATING A NEW BLOCK")
# data = [
#     tnx.get_data()
# ]
# block2 = g_block.get_next_block(data=data)
# # write the block and unspent transaction outputs
# block_chain.write_block(block2)
#
# # create a second new transaction
# print("CREATING MULTI-OUTPUT TRANSACTION")
# tnx2 = client.create_transaction("address2", 500)
# # add more outputs to transaction
# tnx2.add_output("address3", 700)
# tnx2.add_output("address4", 5000)
# client.send_transaction(tnx2)
#
# # create another new block
# print("CREATING NEW BLOCK")
# data = [
#     tnx2.get_data()
# ]
# block3 = block2.get_next_block(data)
# block_chain.write_block(block3)
#
#
# # simulate man-in-middle attack
# print("SIMULATING MAN-IN-MIDDLE ATTACK")
# clean_tnx = client.create_transaction('address5', 100)
# client.send_transaction(clean_tnx)
# print("Transaction before attack is valid?: {}".format(clean_tnx.verify()))
#
# # attack
# print("ATTACKER MODIFYING OUTPUT ADDRESS")
# data = clean_tnx.get_data()
# outputs = data['outputs']
# outputs.append({"address":"eviladdress", "amount": 200})
#
# # Validate the attacked transaction
# print("Transaction is valid?: {}".format(clean_tnx.verify()))



