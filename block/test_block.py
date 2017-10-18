from block import Block
import block
import sys
import block.merkle

# test block class
#block1 = Block(previous_hash='0000000000000000000000000000000000000000000000000000000000000000', transactions='test')
#print(block1.info())

# test the merkle path. Will not be implemented into block class yet
tnx = ['test1', 'test2', 'test3', 'test4', 'test5']
merkleRoot = merkle.findMerkleRoot(tnx)
merklePath = merkle.findMerklePath(tnx, 'test3')
varify = merkle.findTransaction(merklePath, merkleRoot, 'test3')
print(varify)
