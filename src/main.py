import client
from block import Block
from persist import block_chain

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

# Make a new block
new_tnx = client.create_transaction("testdummy1", 400)  # dummy tnx
new_tnx1 = client.create_transaction("testdummy2", 500)  # dummy tnx

data = {  # block data (dict of transactions included in block)
    new_tnx.get_new_id(): new_tnx.get_data(),
    new_tnx1.get_new_id(): new_tnx.get_data()
}
new_block = g_block.get_next_block(data)
block_chain.write_block(new_block)

print(new_tnx1.verify())

#
# # Try to put an invalid block in the block chain
# invalid_block = Block(index=3, data="bad transactions", previous_hash="fakehashy")
# block_chain.write_block(invalid_block)
#
# # Send a new transaction
# sent_tnx = client.send_transaction('test', 3500)  # create/sign/send transaction
# print("Valid Transaction? >>> {}".format(sent_tnx.verify()))  # verify a sent transaction
#
# # Simulate man-in-the-middle attack.
# my_sent_tnx = client.send_transaction('tosomeone', 100)
#
# # man in the middle tries to modify the tnx
# data = my_sent_tnx.get_data()
# message = data['message']
# message['outputs'] = ['myAddress','evilme', 100]  # modify to go to evilme
# print("Transaction after attack: {}".format(my_sent_tnx.get_data()))
#
# # receiving node verifies the corrupt tnx
# print("Valid Transaction? >>> {}".format(my_sent_tnx.verify()))


