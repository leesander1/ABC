from src import client
from src import network

# TODO: if first time opening call network for block chain file
# TODO: otherwise call network for updates
# TODO: if this is the first node on the network and the blockchain has not been created, create the genesis

# Wait for command via interface from user


# Testing purposes below this line #######################################
from src.block import Block
from src.transaction import Transaction

g_block = client.create_genesis() # create genesis block
client.write_block(g_block)  # write it to block chain file
client.write_my_transactions(g_block)  # write all of this nodes received tnxs

sent = client.send_transaction('test', 3500)  # create/sign/send transaction

print(sent.verify())  # verify a sent transaction



