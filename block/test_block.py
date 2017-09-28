from block import Block
import block
import sys

# test variables
print(len(block.version))  # check to see if it is 4 bytes

# test block class
block1 = Block()
block1.transactions = ["123123123123123123", "1231231231312312313"]
block1.merkle_root()

print(block1.merkleRoot)
