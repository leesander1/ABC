from src import client
from src import network


# Load a key pair from data/. If none exist, create a key pair.
client.get_keys()

# Load my address from data/. If none exist, write one.
client.get_address()

# TODO: if first time opening call network for block chain file
# TODO: otherwise call network for updates
# TODO: if this is the first node on the network and the blockchain has not been created, create the genesis

# Wait for command via interface from user


# Testing purposes below this line #######################################
from src.block import Block
from src.transaction import Transaction

g_block = client.create_genesis()
client.write_block(g_block)
client.write_my_transactions(g_block)

sent = client.send_transaction('poop', 7000)
print(sent.verify())



