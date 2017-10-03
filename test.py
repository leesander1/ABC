from block import Block
from core import core


# test block class
block1 = Block(previous_hash='0000000000000000000000000000000000000000000000000000000000000000', transactions='test')
print(block1.info())