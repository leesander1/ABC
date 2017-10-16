from src import client
from src.persist import block_chain
from src.block import Block
# TODO: Check the status of the network, respond accordingly
# TODO: wait for command from user

#####################################################################
#
#
#       TESTING BELOW
#
#
#####################################################################

# Create genesis
g_block = client.create_genesis()
block_chain.write_block(g_block)

# Make a new block
new_tnx = client.create_transaction("testdummy1", 400)  # dummy tnx
new_tnx1 = client.create_transaction("testdummy2", 500)  # dummy tnx

data = {  # block data (dict of transactions included in block)
    0: new_tnx.get_data(),
    1: new_tnx.get_data()
}
new_block = g_block.get_next_block(data)
block_chain.write_block(new_block)

# Try to put an invalid block in the block chain
invalid_block = Block(index=3, data="bad transactions", previous_hash="fakehashy")
block_chain.write_block(invalid_block)

# Send a new transaction
sent_tnx = client.send_transaction('test', 3500)  # create/sign/send transaction
print("Valid Transaction? >>> {}".format(sent_tnx.verify()))  # verify a sent transaction



