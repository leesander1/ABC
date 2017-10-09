from block import Block
from client import block_chain
import json

block_chain.append(Block.create_genesis())

tnx = json.loads(block_chain[0].get_transactions())

print(tnx['inputs'])