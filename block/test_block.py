from block import Block
import block
import sys


# test block class
block1 = Block(previous_hash='0000000000000000000000000000000000000000000000000000000000000000', transactions='test')
print(block1.info())

print(block1.merkleRoot)
