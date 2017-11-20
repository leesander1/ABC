import client
from persist import block_chain
from persist import abc_key as keys

from src.cli import CLI
# TODO: Check the status of the network, respond accordingly
# TODO: wait for command from user

# cli = CLI()
# cli.cmdloop()
#####################################################################
#
#
#       TESTING BELOW
#
#
#####################################################################

# Create genesis
print("Creating Genesis Block")
g_block = client.create_genesis()

# create new transaction and "send" it
print("Sending transaction to address1 for 400 ABC")
tnx = client.send_transaction("address1", 400)

# create a new block
print("CREATING A NEW BLOCK")
data = [
    tnx.get_data()
]
block2 = g_block.get_next_block(transactions=data)
# write the block and unspent transaction outputs
block_chain.write_block(block2)
block_chain.write_unspent_outputs(block2, keys.get_public_key())

# create a second new transaction
print("CREATING MULTI-OUTPUT TRANSACTION")
tnx2 = client.send_transaction("address2", 500)


# create another new block
print("CREATING NEW BLOCK")
data = [
    tnx2.get_data()
]
block3 = block2.get_next_block(data)
block_chain.write_block(block3)
block_chain.write_unspent_outputs(block3, keys.get_public_key())


# simulate man-in-middle attack
print("SIMULATING MAN-IN-MIDDLE ATTACK")
clean_tnx = client.send_transaction('address5', 100)
print("Transaction before attack is valid?: {}".format(clean_tnx.verify()))

# attack
print("ATTACKER MODIFYING OUTPUT ADDRESS")
data = clean_tnx.get_data()
outputs = data['outputs']
outputs.append({"address":"eviladdress", "amount": 200})

# Validate the attacked transaction
print("Transaction is valid?: {}".format(clean_tnx.verify()))



